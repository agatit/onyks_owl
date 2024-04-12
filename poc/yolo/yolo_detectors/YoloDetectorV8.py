from functools import singledispatchmethod

import numpy as np
from ultralytics import YOLO

from yolo.DetectionResult import DetectionResult
from yolo.YoloFormat import BoundingBox, YoloFormat
from yolo.yolo_detectors.YoloDetector import YoloDetector


class YoloDetectorV8(YoloDetector):

    def __init__(self, model_path: str, confidence_threshold: float = 0.25, batch_size: int = 300,
                 verbose: bool = False, classes: list[int] = None, tracking: bool = False):
        super().__init__(model_path, confidence_threshold, batch_size, verbose, classes)
        self.tracking = tracking

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
        if len(images) < 1:
            return []

        results = self._model.track(images, conf=self.confidence_threshold, verbose=self.verbose, persist=True)
        return self._detection_results_from_detections(results)

    @__call__.register
    def _(self, image: np.ndarray) -> list[list[DetectionResult]]:
        if image is None:
            return None

        yolo_detection_result = self._model.track(image, conf=self.confidence_threshold, verbose=self.verbose,
                                                  persist=True)
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
            for cls, conf, xyxy, xywhn, track_id in zip(boxes.cls, boxes.conf, boxes.xyxy, boxes.xywhn, boxes.id):
                track_id = int(track_id.item())
                cls, conf = int(cls.item()), conf.item()

                class_name = results.names[cls]

                x1, y1 = int(xyxy[0].item()), int(xyxy[1].item())
                x2, y2 = int(xyxy[2].item()), int(xyxy[3].item())

                x_center, y_center = xywhn[0].item(), xywhn[1].item()
                width, height = xywhn[2].item(), xywhn[3].item()

                bounding_box = BoundingBox(y1, y2, x1, x2)
                yolo_format = YoloFormat(cls, x_center, y_center, width, height)
                detection_result = DetectionResult(class_name, bounding_box, yolo_format, conf, track_id)

                detection_results.append(detection_result)

            all_results.append(detection_results)

        return all_results
