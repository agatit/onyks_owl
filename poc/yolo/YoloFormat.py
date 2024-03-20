from dataclasses import dataclass


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

    def to_yolo_txt_line(self) -> str:
        fields = [self.class_id, self.x_center, self.y_center, self.width, self.height]
        _str = " ".join(str(_field) for _field in fields)
        return _str + '\n'

    @classmethod
    def from_yolo_txt(cls, str_line: str) -> "YoloFormat":
        split = str_line.split()

        class_id, x_center, y_center, width, height = split
        return cls(int(class_id), float(x_center), float(y_center), float(width), float(height))

