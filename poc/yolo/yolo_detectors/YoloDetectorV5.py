import pathlib
import platform
from contextlib import contextmanager
from functools import singledispatchmethod
from typing import Any

import numpy as np
import torch
from ultralytics import YOLO

from yolo.DetectionResult import DetectionResult
from yolo.YoloFormat import BoundingBox, YoloFormat
from yolo.yolo_detectors.YoloDetector import YoloDetector


# bug - https://github.com/ultralytics/yolov5/issues/10240#issuecomment-1927109491
@contextmanager
def set_posix_windows():
    posix_backup = pathlib.PosixPath
    try:
        pathlib.PosixPath = pathlib.WindowsPath
        yield
    finally:
        pathlib.PosixPath = posix_backup



class YoloDetectorV5(YoloDetector):

    @classmethod
    def _initialize_model(cls, model_path: str) -> tuple[Any, dict, str]:
        # model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

        if platform.system() == "Windows":
            with set_posix_windows():
                model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        else:
            model = torch.hub.load('ultralytics/yolov8', 'custom', path=model_path)

        classes = model.names
        device = 'cuda' if cls.check_if_cuda_is_available() else 'cpu'
        model.to(device)

        return model, classes, device

    @singledispatchmethod
    def __call__(self):
        pass

    @__call__.register
    def _(self, images: list) -> list[list[DetectionResult]]:
        results = self._model(images)
        return self._detection_results_from_detections(results)

    @__call__.register
    def _(self, image: np.ndarray) -> list[list[DetectionResult]]:
        yolo_detection_result = self._model(image)
        return self._detection_results_from_detections(yolo_detection_result)

    def _detection_results_from_detections(self, results) -> list[DetectionResult]:
        classes = self.classes

        all_results = []
        for preds, xywhns in zip(results.pred, results.xywhn):
            detection_results = []

            # check if no predictions
            if len(preds) < 1:
                all_results.append(detection_results)
                continue

            for pred, xywhn in zip(preds, xywhns):
                pred_int = [int(i) for i in pred]

                x1, y1 = pred_int[0], pred_int[1]
                x2, y2 = pred_int[2], pred_int[3]
                confidence = float(pred[4])
                class_id = pred_int[5]
                class_name = classes[class_id]

                float_xywhn = [float(i) for i in xywhn[:4]]
                x_center, y_center = float_xywhn[0], float_xywhn[1]
                width, height = float_xywhn[2], float_xywhn[3]

                bounding_box = BoundingBox(y1, y2, x1, x2)
                yolo_format = YoloFormat(class_id, x_center, y_center, width, height)
                detection_result = DetectionResult(class_name, bounding_box, yolo_format, confidence)

                detection_results.append(detection_result)

            all_results.append(detection_results)

        return all_results

