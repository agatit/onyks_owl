from dataclasses import dataclass, field

import cv2
import numpy as np

from display.opencv_wrappers import draw_text, draw_rectangle


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

    @classmethod
    def from_bounding_box(cls, class_id: int, original_width: int, original_height: int,
                          bounding_box: BoundingBox):
        box_width_pixels = abs(bounding_box.x2 - bounding_box.x1)
        box_height_pixels = abs(bounding_box.y2 - bounding_box.y1)
        x_center_pixels = bounding_box.x1 + box_width_pixels // 2
        y_center_pixels = bounding_box.y1 + box_height_pixels // 2

        x_center = x_center_pixels / original_width
        y_center = y_center_pixels / original_height
        width = box_width_pixels / original_width
        height = box_height_pixels / original_height

        return cls(class_id, x_center, y_center, width, height)

    def to_bounding_box(self, original_width: int, original_height: int) -> BoundingBox:
        box_x_center_pixels = int(original_width * self.x_center)
        box_y_center_pixels = int(original_height * self.y_center)
        box_width_pixels = int(original_width * self.width)
        box_height_pixels = int(original_height * self.height)

        x1 = int(box_x_center_pixels - box_width_pixels / 2)
        x2 = int(box_x_center_pixels + box_width_pixels / 2)
        y1 = int(box_y_center_pixels - box_height_pixels / 2)
        y2 = int(box_y_center_pixels + box_height_pixels / 2)

        return BoundingBox(y1, y2, x1, x2)


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
