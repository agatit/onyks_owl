from dataclasses import dataclass
from typing import ClassVar

import numpy as np


@dataclass
class BoundingBox:
    y1: int
    y2: int
    x1: int
    x2: int

    @classmethod
    def from_x1y1_x2y2(cls, x1y1: tuple[int, int], x2y2: tuple[int, int]):
        return cls(x1y1[1], x2y2[1], x1y1[0], x2y2[0])


@dataclass
class YoloFormat:
    IOU_SIMILARITY_THRESHOLD: ClassVar[float] = 0.8

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

    def crop(self, image: np.ndarray, original_width: int, original_height: int) -> np.ndarray:
        bounding_box = self.to_bounding_box(original_width, original_height)
        return image[bounding_box.y1:bounding_box.y2, bounding_box.x1:bounding_box.x2]

    def to_yolo_txt_line(self) -> str:
        fields = [self.class_id, self.x_center, self.y_center, self.width, self.height]
        _str = " ".join(str(_field) for _field in fields)
        return _str + '\n'

    @classmethod
    def from_yolo_txt(cls, str_line: str) -> "YoloFormat":
        split = str_line.split()

        class_id, x_center, y_center, width, height = split
        return cls(int(class_id), float(x_center), float(y_center), float(width), float(height))

    @classmethod
    def load_from_file(cls, file) -> list["YoloFormat"]:
        lines = file.readlines()
        return [YoloFormat.from_yolo_txt(line) for line in lines]

    def __eq__(self, other):
        iou = self._calculate_iou(self, other)
        return iou > self.IOU_SIMILARITY_THRESHOLD

    @staticmethod
    def _calculate_iou(format1: "YoloFormat", format2: "YoloFormat") -> float:
        # (center_x, center_y, width, height)

        # Convert normalized coordinates to absolute coordinates
        x1_box1 = format1.x_center - format1.width / 2
        y1_box1 = format1.y_center - format1.height / 2
        x2_box1 = format1.x_center + format1.width / 2
        y2_box1 = format1.y_center + format1.height / 2

        x1_box2 = format2.x_center - format2.width / 2
        y1_box2 = format2.y_center - format2.height / 2
        x2_box2 = format2.x_center + format2.width / 2
        y2_box2 = format2.y_center + format2.height / 2

        # Calculate intersection coordinates
        x_left = max(x1_box1, x1_box2)
        y_top = max(y1_box1, y1_box2)
        x_right = min(x2_box1, x2_box2)
        y_bottom = min(y2_box1, y2_box2)

        # Calculate intersection area
        intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

        # Calculate areas of each bounding box
        area_box1 = (x2_box1 - x1_box1) * (y2_box1 - y1_box1)
        area_box2 = (x2_box2 - x1_box2) * (y2_box2 - y1_box2)

        # Calculate union area
        union_area = area_box1 + area_box2 - intersection_area

        # Calculate IoU
        iou = intersection_area / union_area if union_area > 0 else 0

        return iou
