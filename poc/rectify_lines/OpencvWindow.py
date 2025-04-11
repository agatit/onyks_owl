from dataclasses import dataclass
from typing import ClassVar

import cv2
import numpy as np


@dataclass
class MouseEvent:
    event: int
    x: int
    y: int
    flags: int
    userdata: any


@dataclass
class OpencvWindow:
    PAINT_DOT_KWARGS: ClassVar[dict] = {
        "radius": 5,
        "thickness": -1,
        "color": (0, 255, 255)
    }

    name: str
    img: np.ndarray

    def __post_init__(self):
        self._original_img = self.img.copy()
        self.last_mouse_event: MouseEvent = None

    def paint_dot(self, x: int, y: int):
        cv2.circle(
            img=self.img,
            center=(x, y),
            **self.PAINT_DOT_KWARGS
        )
        self.show()

    def reload(self):
        self.img = self._original_img.copy()
        self.show()

    def show(self):
        cv2.imshow(self.name, self.img)
