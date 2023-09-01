from itertools import cycle

import cv2
import numpy as np


class ImageEventHandler:
    def __init__(self, image, window_name, *line_types):
        self.image = image
        self.window_name = window_name
        self.line_types = line_types

        self.line_types_cycle = cycle(line_types)
        self.current_line_type = next(self.line_types_cycle)

        self.dots = []
        self.image_copy = self.image.copy()

        height = int(image.shape[0] * 5 / 100)
        width = int(image.shape[1] * 15 / 100)
        size = (height, width, 3)
        self.status_image = StatusImage(size)

    def mouse_callback(self):
        def wrapper(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN and len(self.dots) != self.current_line_type.max_dots_number:
                self.dots.append((x, y))
                self.paint_dot(x, y)

            elif event == cv2.EVENT_LBUTTONDOWN and len(self.dots) == self.current_line_type.max_dots_number:
                self.reload()

            if event == cv2.EVENT_RBUTTONDOWN:
                self.current_line_type = next(self.line_types_cycle)
                self.reload()

            self.display_line_type_state()

        return wrapper

    def paint_dot(self, x, y):
        circle_kwargs = {
            "img": self.image,
            "center": (x, y),
            "radius": 5,
            "thickness": -1,
            "color": (0, 255, 255)
        }

        cv2.circle(**circle_kwargs)
        cv2.imshow(self.window_name, self.image)

    def display_line_type_state(self):
        self.status_image.reload()
        put_text_kwargs = {
            "img": self.status_image.background,
            "text": f"{self.current_line_type.type}:{len(self.dots)}",
            "org": (0, 25),
            "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
            "fontScale": 1,
            "thickness": 3,
            "color": (0, 0, 255)
        }
        cv2.putText(**put_text_kwargs)

        self.status_image.overlay(self.image)
        cv2.imshow(self.window_name, self.image)

    def save_current_dots(self):
        self.current_line_type.lines.append(self.dots)
        self.reload()

    def reload(self):
        self.image = self.image_copy.copy()
        self.dots = []


class StatusImage:

    def __init__(self, shape):
        self.background = np.full(shape, 255, dtype=np.uint8)
        self.background_copy = self.background.copy()

    def overlay(self, image):
        shape = self.background.shape
        image[:shape[0], :shape[1]] = self.background

    def reload(self):
        self.background = self.background_copy.copy()
