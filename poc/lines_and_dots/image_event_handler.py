from itertools import cycle

import cv2


class ImageEventHandler:
    def __init__(self, image, window_name, *line_types):
        self.image = image
        self.window_name = window_name
        self.line_types = line_types
        self.line_types_cycle = cycle(line_types)

        self.current_line_type = next(self.line_types_cycle)

        self.dots = []
        self.image_copy = self.image.copy()

    def mouse_callback(self):
        def wrapper(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
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

            if event == cv2.EVENT_RBUTTONDOWN:
                self.current_line_type = next(self.line_types_cycle)

                self.reload()
                self.display_current_line_type()

        return wrapper

    def save_current_dots(self):
        self.current_line_type.lines.append(self.dots)
        self.reload()

    def display_current_line_type(self):
        put_text_kwargs = {
            "img": self.image,
            "text": self.current_line_type.type,
            "org": (0, 25),
            "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
            "fontScale": 1,
            "thickness": 3,
            "color": (0, 0, 255)
        }

        cv2.putText(**put_text_kwargs)
        cv2.imshow(self.window_name, self.image)

    def reload(self):
        self.image = self.image_copy.copy()
        self.dots = []
