from typing import Union, Any

import cv2
import numpy as np


def scale_image_by_percent(image: np.ndarray, percent: int) -> np.ndarray:
    image = image.copy()

    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def scale_point_by_percent(point: Union[list, tuple], percent: int) -> tuple[int, int]:
    x = int(point[0] * percent / 100)
    y = int(point[1] * percent / 100)
    return x, y


def random_color_256() -> Union[tuple[Any], tuple[int, int, int]]:
    color = np.random.randint(0, 256, (3,), dtype=int)
    return tuple((i.item() for i in color))
