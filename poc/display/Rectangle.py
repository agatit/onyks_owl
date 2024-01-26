from dataclasses import dataclass, asdict, field

import cv2
import numpy as np


@dataclass
class RectangleStyle:
    # BGR color
    color: tuple[int, int, int] = (0, 0, 255)
    thickness: int = 2


class RectangleDisplay:

    @classmethod
    def draw(cls, image: np.ndarray, p1: tuple, p2: tuple, style: RectangleStyle) -> np.ndarray:
        return cv2.rectangle(image.copy(), p1, p2, **asdict(style))

