from dataclasses import dataclass, field

import cv2
from cv2 import VideoCapture

from stream.loaders.Loader import Loader


@dataclass
class VideoLoader(Loader):

    def get_image_gen(self):
        input_path_str = str(self.input_path)
        video_capture = cv2.VideoCapture(input_path_str)

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if ret:
                yield frame
            else:
                break

        video_capture.release()
