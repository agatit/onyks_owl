from dataclasses import dataclass, field

import cv2
import numpy as np


@dataclass
class BoundingBox:
    y1: int
    y2: int
    x1: int
    x2: int


@dataclass
class DetectionResult:
    label_name: str
    bounding_box: BoundingBox
    confidence: float

    padding = {
        'x': 20,
        'y': 25
    }
    precission = 3

    def draw_on_image(self, image: np.ndarray):
        image = image.copy()

        box = self.bounding_box
        image = cv2.rectangle(image, (box.x1, box.y1), (box.x2, box.y2), (0, 0, 255), 2)

        padding = self.padding
        text = f"{self.label_name}: {round(self.confidence, self.precission)}"

        # check if text can be drown outside a rectangle
        if box.y1 <= padding['y']:
            placement = (box.x1, box.y1 + padding['y'])
        else:
            placement = (box.x1, box.y1 - padding['y'])

        image = cv2.putText(image, text, placement, cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255), 2)
        return image
