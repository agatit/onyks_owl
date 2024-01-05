from dataclasses import dataclass

import cv2 as cv
import numpy as np
import torch

from yolo.DetectionResult import DetectionResult, BoundingBox


class YoloDetector:
    LABELS = ["vertical_text", "horizontal_text", "container_corners", "container", "railcar_boogie",
              "railcar_text", "railcar_gap"]

    RESULT_COLS = ["name", "ymin", "ymax", "xmin", "xmax", "confidence"]
    CORDS_COLS = ["ymin", "ymax", "xmin", "xmax"]

    def __init__(self, model_path, confidence_threshold=0):
        self.model_path = model_path
        self.confidence_threshhold = confidence_threshold

        model, classes, device = self.initialize_model(self.model_path)
        self.model = model
        self.classes = classes
        self.device = device

    @classmethod
    def initialize_model(cls, model_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        classes = model.names
        device = 'cuda' if cls.check_if_cuda_is_avaible() else 'cpu'

        model.to(device)

        return model, classes, device

    def detect_image(self, image: np.ndarray, selected_labels: list[str]) -> list[DetectionResult]:
        model = self.model
        detection_result = model(image)

        # output format
        results_df = detection_result.pandas().xyxy[0]
        results_df = results_df[self.RESULT_COLS]

        # filter labels
        results_df = results_df[results_df["name"].isin(selected_labels)]

        # float cords to int
        convert_type = {col: "int32" for col in self.CORDS_COLS}
        results_df = results_df.astype(convert_type)

        results = []
        threshhold = self.confidence_threshhold
        for i in results_df.values.tolist():
            confidence = i[5]

            if confidence < threshhold:
                continue

            name = i[0]
            bounding_box = BoundingBox(*i[1:5])
            detection_result = DetectionResult(name, bounding_box, confidence)

            results.append(detection_result)

        return results

    def enable_multiprocessing(self) -> None:
        self.model.share_memory()

    @classmethod
    def check_if_cuda_is_avaible(cls) -> bool:
        return torch.cuda.is_available()
