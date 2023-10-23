from contextlib import contextmanager
from typing import Callable

import cv2


# def video_stream(input_capture):
#     while input_capture.isOpened():
#         ret, frame = input_capture.read()
#         if ret:
#             yield frame
#         else:
#             break


@contextmanager
def open_video_capture(source: str):
    video_capture = cv2.VideoCapture(source)
    try:
        yield video_capture
    finally:
        video_capture.release()
