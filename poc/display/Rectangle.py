from dataclasses import dataclass, asdict

import cv2
import numpy as np


@dataclass
class RectangleStyle:
    color: tuple[int, int, int]
    thickness: int


class RectangleDisplay:

    @classmethod
    def draw(cls, image: np.ndarray, p1: tuple, p2: tuple, style: RectangleStyle) -> np.ndarray:
        return cv2.rectangle(image.copy(), p1, p2, **asdict(style))

