import glob
from typing import Protocol, Generator

import cv2
import numpy as np


class ImageGenerator(Protocol):
    def __call__(self, source: str) -> Generator[np.ndarray, None, None]:
        ...


def video_gen(source: str) -> Generator[np.ndarray, None, None]:
    cap = cv2.VideoCapture(source)

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            yield frame
        else:
            break

    cap.release()


def image_dir_gen(source: str, extension: str = ".jpg") -> Generator[np.ndarray, None, None]:
    glob_mask = f"{source}/*{extension}"
    for image_path in glob.glob(glob_mask):
        image = cv2.imread(image_path)
        yield image
