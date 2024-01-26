import cv2
import numpy as np


# color BGR

def draw_rectangle(image: np.ndarray, p1: tuple, p2: tuple, color: tuple = (0, 0, 255),
                   thickness: int = 3, **kwargs) -> np.ndarray:
    return cv2.rectangle(image.copy(), p1, p2, color, thickness, **kwargs)


def draw_text(image: np.ndarray, text: str, org: tuple, *args, font_face: int = cv2.FONT_HERSHEY_SIMPLEX,
              font_scale: float = 0.8, color: tuple = (0, 0, 255), thickness: int = 2, **kwargs) -> np.ndarray:
    return cv2.putText(image.copy(), text, org, font_face, font_scale, color, thickness, *args, **kwargs)
