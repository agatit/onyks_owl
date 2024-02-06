import pathlib
import platform
from contextlib import contextmanager
from dataclasses import dataclass

import cv2 as cv
import numpy as np
import torch

from yolo.DetectionResult import DetectionResult, BoundingBox, YoloFormat


# bug - https://github.com/ultralytics/yolov5/issues/10240#issuecomment-1927109491
@contextmanager
def set_posix_windows():
    posix_backup = pathlib.PosixPath
    try:
        pathlib.PosixPath = pathlib.WindowsPath
        yield
    finally:
        pathlib.PosixPath = posix_backup


class YoloDetector:
    XYXY_COLS = ["class", "name", "confidence", "ymin", "ymax", "xmin", "xmax"]
    XYWHN_COLS = ["xcenter", "ycenter", "width", "height"]

    INT_COLS = ["class", "ymin", "ymax", "xmin", "xmax"]

    def __init__(self, model_path: str, confidence_threshold: float = 0.25):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold

        model, classes, device = self.initialize_model(self.model_path)
        self.model = model
        self.classes = classes
        self.device = device

        self.labels = list(self.classes.values())

    @classmethod
    def initialize_model(cls, model_path: str):
        # model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

        with set_posix_windows():
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

        classes = model.names
        device = 'cuda' if cls.check_if_cuda_is_available() else 'cpu'

        model.to(device)

        return model, classes, device

    def detect_image(self, image: np.ndarray, selected_labels: list[str]) -> list[DetectionResult]:
        yolo_detection_result = self.model(image)

        # output to pandas format
        results_df = yolo_detection_result.pandas()

        xyxy = results_df.xyxy[0]  # xmin, ymin, xmax, ymax
        xyxy = xyxy[self.XYXY_COLS]

        xywhn = results_df.xywhn[0]  # xcenter, ycenter, width, height, normalized
        xywhn = xywhn[self.XYWHN_COLS]

        # join by index
        results_df = xyxy.join(xywhn, lsuffix='_xyxy', rsuffix='_xywhn')

        # filter
        results_df = results_df[results_df["name"].isin(selected_labels)]
        results_df = results_df[results_df["confidence"] > self.confidence_threshold]

        # float cords to int
        convert_type = {col: "int32" for col in self.INT_COLS}
        results_df = results_df.astype(convert_type)

        return [self._map_cols_to_detection_result(cols) for cols in results_df.to_dict('index').values()]

    @staticmethod
    def _map_cols_to_detection_result(cols: dict) -> DetectionResult:
        kwargs = {
            "x1": cols["xmin"],
            "y1": cols["ymin"],
            "x2": cols["xmax"],
            "y2": cols["ymax"],
        }
        bounding_box = BoundingBox(**kwargs)

        kwargs = {
            "class_id": cols["class"],
            "x_center": cols["xcenter"],
            "y_center": cols["ycenter"],
            "width": cols["width"],
            "height": cols["height"],
        }
        yolo_format = YoloFormat(**kwargs)

        kwargs = {
            "class_name": cols["name"],
            "bounding_box": bounding_box,
            "yolo_format": yolo_format,
            "confidence": cols["confidence"],
        }
        return DetectionResult(**kwargs)

    def enable_multiprocessing(self) -> None:
        self.model.share_memory()

    @staticmethod
    def check_if_cuda_is_available() -> bool:
        return torch.cuda.is_available()
