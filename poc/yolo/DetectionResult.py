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
class YoloFormat:
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float


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
        image = cv2.rectangle(image, (box.x1, box.y1), (box.x2, box.y2), (0, 0, 255), 2)

        text = f"{self.class_name}: {round(self.confidence, self.precision)}"

        # check if text can be drawn outside a rectangle
        padding = self.padding
        if box.y1 <= padding['y']:
            placement = (box.x1, box.y1 + padding['y'])
        else:
            placement = (box.x1, box.y1 - padding['y'])

        image = cv2.putText(image, text, placement, cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255), 2)
        return image
