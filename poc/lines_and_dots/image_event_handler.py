from dataclasses import dataclass

import cv2
import numpy as np


class ImageEventHandler:
    def __init__(self, image, window_name):
        self.image = image
        self.window_name = window_name

        self.image_copy = self.image.copy()

    def mouse_callback(self):
        # TODO do struktury callbacki
        def wrapper(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                put_text_kwargs = {
                    "img": self.image,
                    "text": f"left:{(x, y)}",
                    "org": (x, y),
                    "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
                    "fontScale": 2,
                    "color": (255, 0, 0)
                }

                cv2.putText(**put_text_kwargs)
                cv2.imshow(self.window_name, self.image)

            if event == cv2.EVENT_RBUTTONDOWN:
                self.reload_image()

        return wrapper

    def reload_image(self):
        self.image = self.image_copy.copy()
        cv2.imshow(self.window_name, self.image)
