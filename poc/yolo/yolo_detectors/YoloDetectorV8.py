from functools import singledispatchmethod

import numpy as np
from ultralytics import YOLO

from yolo.DetectionResult import DetectionResult
from yolo.YoloFormat import BoundingBox, YoloFormat
from yolo.yolo_detectors.YoloDetector import YoloDetector


class YoloDetectorV8(YoloDetector):
    @classmethod
    def _initialize_model(cls, model_path: str) -> tuple:
        model = YOLO(model_path)

        classes = model.names
        device = 'cuda' if cls.check_if_cuda_is_available() else 'cpu'
        model.to(device)

        return model, classes, device

    @singledispatchmethod
    def __call__(self) -> list[list[DetectionResult]]:
        pass

    @__call__.register
    def _(self, images: list) -> list[list[DetectionResult]]:
        results = self._model(images, conf=self.confidence_threshold)
        return self._detection_results_from_detections(results)

    @__call__.register
    def _(self, image: np.ndarray) -> list[list[DetectionResult]]:
        yolo_detection_result = self._model(image, conf=self.confidence_threshold)
        return self._detection_results_from_detections(yolo_detection_result)

    @staticmethod
    def _detection_results_from_detections(batch) -> list[list[DetectionResult]]:
        all_results = []
        for results in batch:
            detection_results = []

            if len(results) < 1:
                all_results.append(detection_results)
                continue

            boxes = results.boxes
            for cls, conf, xyxy, xywhn in zip(boxes.cls, boxes.conf, boxes.xyxy, boxes.xywhn):
                cls, conf = int(cls.item()), conf.item()

                class_name = results.names[cls]

                x1, y1 = int(xyxy[0].item()), int(xyxy[1].item())
                x2, y2 = int(xyxy[2].item()), int(xyxy[3].item())

                x_center, y_center = xywhn[0].item(), xywhn[1].item()
                width, height = xywhn[2].item(), xywhn[3].item()

                bounding_box = BoundingBox(y1, y2, x1, x2)
                yolo_format = YoloFormat(cls, x_center, y_center, width, height)
                detection_result = DetectionResult(class_name, bounding_box, yolo_format, conf)

                detection_results.append(detection_result)

            all_results.append(detection_results)

        return all_results
