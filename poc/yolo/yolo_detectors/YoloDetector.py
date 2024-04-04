import abc
from abc import ABC
from functools import singledispatchmethod
from typing import Any

import numpy as np
import torch

from yolo.DetectionResult import DetectionResult


class YoloDetector(ABC):
    def __init__(self, model_path: str, confidence_threshold: float = 0.25, batch_size=300):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.batch_size = batch_size

        model, classes, device = self._initialize_model(self.model_path)
        self._model = model
        self.classes = classes
        self.device = device

        self._model.conf = self.confidence_threshold

        self.selected_classes = self.classes.keys()

    @classmethod
    @abc.abstractmethod
    # return Model, classes, device
    def _initialize_model(cls, model_path: str) -> tuple[Any, dict, str]:
        pass

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

    def select_classes(self, new_classes: list[int]) -> None:
        self._model.classes = list(new_classes)

    @staticmethod
    def check_if_cuda_is_available() -> bool:
        return torch.cuda.is_available()
