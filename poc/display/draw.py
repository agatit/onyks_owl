from typing import Sequence

import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX
THICKNESS = 1


def put_text_on_image_margin(image: np.ndarray, texts: Sequence[str], char_height_ratio: float = 0.3) -> np.ndarray:
    """

    Args:
        image ():
        texts ():
        char_height_ratio ():

    Returns:
        image with text on its margin
    """
    
    image_copy = image.copy()
    original_height, original_width, original_depth = image_copy.shape

    font_pixel_height = original_height // len(texts)
    font_pixel_height = int(font_pixel_height * char_height_ratio)
    font_scale = cv2.getFontScaleFromHeight(
        fontFace=FONT,
        pixelHeight=font_pixel_height,
        thickness=THICKNESS
    )

    longest_text = max(texts, key=len)
    (text_width, text_height), baseline = cv2.getTextSize(
        text=longest_text,
        fontScale=font_scale,
        fontFace=FONT,
        thickness=THICKNESS
    )

    margin = np.ones((original_height, text_width, original_depth)) * 255
    result = np.append(image_copy, margin, axis=1)

    for text_index, text in enumerate(texts, start=1):
        org = (original_width, font_pixel_height * text_index)
        cv2.putText(
            img=result,
            text=text,
            org=org,
            fontFace=FONT,
            fontScale=font_scale,
            color=(0, 0, 0),
            thickness=THICKNESS,
        )

    return result
