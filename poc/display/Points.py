from dataclasses import dataclass, asdict

import cv2
import numpy as np

from display.utils import scale_image_by_percent


@dataclass
class PointStyle:
    radius: int
    thickness: int
    color: tuple[int, int, int]


@dataclass
class PointDisplay:
    lines: np.ndarray
    style: PointStyle


def display_image_with_points(image: np.ndarray, window_name: str, display_scale: int = 70,
                              *point_displays: PointDisplay):
    img = image.copy()

    for dot_display in point_displays:
        for line in dot_display.lines.astype(int):
            for point in line:
                cv2.circle(img, center=point, **asdict(dot_display.style))

    cv2.imshow(window_name, scale_image_by_percent(img, display_scale))
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)
