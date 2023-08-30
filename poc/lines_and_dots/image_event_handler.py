from dataclasses import dataclass

import cv2
import numpy as np


class ImageEventHandler:
    def __init__(self, image, window_name):
        self.image = image
        self.window_name = window_name
        self.image_copy = self.image.copy()

        self.left_click_counter = 1
        self.line_start_end_points = []
        self.dots = []

    def mouse_callback(self):
        # TODO do struktury callbacki
        def wrapper(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                circle_kwargs = {
                    "img": self.image,
                    "center": (x, y),
                    "radius": 5,
                    "thickness": -1,
                    "color": (0, 0, 255)
                }

                counter = self.left_click_counter
                if counter % 3 == 0:
                    self.line_start_end_points = []
                    self.reload_image()
                elif counter % 3 == 2:
                    start_line_point = self.line_start_end_points[0]
                    end_line_point = (x, y)
                    self.line_start_end_points.append(end_line_point)

                    line_kwargs = {
                        "img": self.image,
                        "pt1": start_line_point,
                        "pt2": end_line_point,
                        "thickness": 5,
                        "color": (0, 0, 255)
                    }

                    cv2.line(**line_kwargs)
                else:
                    start_line_point = (x, y)
                    self.line_start_end_points.append(start_line_point)

                    cv2.circle(**circle_kwargs)

                self.left_click_counter = counter + 1
                cv2.imshow(self.window_name, self.image)

            if event == cv2.EVENT_RBUTTONDOWN and len(self.line_start_end_points) >= 2:
                circle_kwargs = {
                    "img": self.image,
                    "center": (x, y),
                    "radius": 5,
                    "thickness": -1,
                    "color": (0, 255, 255)
                }

                self.dots.append((x, y))

                cv2.circle(**circle_kwargs)
                cv2.imshow(self.window_name, self.image)

        return wrapper

    def reload_image(self):
        self.image = self.image_copy.copy()
        self.line_start_end_points = []
        self.dots = []

        cv2.imshow(self.window_name, self.image)
