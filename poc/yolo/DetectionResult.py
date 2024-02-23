from dataclasses import dataclass

import numpy as np

from display.opencv_wrappers import draw_text, draw_rectangle
from yolo.YoloFormat import BoundingBox, YoloFormat


@dataclass
class DetectionResult:
    class_name: str
    bounding_box: BoundingBox
    yolo_format: YoloFormat
    confidence: float

    padding = {
        'x': 20,
        'y': 25
    }
    precision = 3

    def draw_on_image(self, image: np.ndarray):
        image = image.copy()

        box = self.bounding_box
        p1 = (box.x1, box.y1)
        p2 = (box.x2, box.y2)
        image = draw_rectangle(image, p1, p2)

        # check if text can be drawn outside a rectangle
        padding = self.padding
        if box.y1 <= padding['y']:
            placement = (box.x1, box.y1 + padding['y'])
        else:
            placement = (box.x1, box.y1 - padding['y'])

        text = f"{self.class_name}: {round(self.confidence, self.precision)}"
        image = draw_text(image, text, placement)

        return image
