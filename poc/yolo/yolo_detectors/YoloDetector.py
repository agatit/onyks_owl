import abc
from abc import ABC
from functools import singledispatchmethod
from typing import Any

import numpy as np
import torch
from ultralytics import YOLO

from yolo.DetectionResult import DetectionResult


class YoloDetector(ABC):
    def __init__(self, model_path: str, confidence_threshold: float = 0.25, batch_size: int = 300,
                 verbose: bool = False, selected_classes: list[int] = None):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.batch_size = batch_size
        self.verbose = verbose

        model, classes, device = self._initialize_model(self.model_path)
        self._model = model
        self.classes = classes
        self.device = device

        self._model.conf = self.confidence_threshold

        self.selected_classes = self.classes.keys()

        if selected_classes is not None:
            self.select_classes(selected_classes)

    @classmethod
    def _initialize_model(cls, model_path: str) -> tuple[Any, dict, str]:
        model = YOLO(model_path)

        classes = model.names
        device = 'cuda' if cls.check_if_cuda_is_available() else 'cpu'
        model.to(device)

        return model, classes, device

    @singledispatchmethod
    def __call__(self) -> list[list[DetectionResult]]:
        pass

    @abc.abstractmethod
    @__call__.register
    def _(self, images: list) -> list[list[DetectionResult]]:
        pass

    @abc.abstractmethod
    @__call__.register
    def _(self, image: np.ndarray) -> list[list[DetectionResult]]:
        pass

    def track(self, image: np.ndarray, *args, **kwargs) -> Any:
        return self._model.track(image, *args, verbose=self.verbose, **kwargs)

    def select_classes(self, new_classes: list[int]) -> None:
        self._model.classes = list(new_classes)

    @staticmethod
    def check_if_cuda_is_available() -> bool:
        return torch.cuda.is_available()
