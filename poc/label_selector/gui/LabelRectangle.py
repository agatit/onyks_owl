from dataclasses import dataclass, field

from yolo.YoloFormat import BoundingBox


@dataclass
class LabelRectangle:
    label_id: int
    label_text: str
    bounding_box: BoundingBox

    full_label: str = field(init=False, repr=False)

    def __post_init__(self):
        self.full_label = f"{self.label_id}_{self.label_text}"
