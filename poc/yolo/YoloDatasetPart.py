import uuid
from dataclasses import dataclass, field
from pathlib import Path

from yolo.YoloFormat import YoloFormat


@dataclass
class YoloDatasetPart:
    original_image_path: Path
    yolo_formats: list[YoloFormat] = field(default_factory=list)

    _id: uuid.UUID = field(init=False)
    output_file_name: str = field(init=False)

    def __post_init__(self):
        self._id = uuid.uuid1()
        self.output_file_name = self._id.hex
