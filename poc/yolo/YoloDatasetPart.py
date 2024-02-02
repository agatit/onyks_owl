import uuid
from dataclasses import dataclass, field
from pathlib import Path

from yolo.DetectionResult import YoloFormat


@dataclass
class YoloDatasetPart:
    yolo_formats: list[YoloFormat]
    original_image_path: Path

    _id: uuid.UUID = field(init=False)
    output_file_name: str = field(init=False)

    def __post_init__(self):
        self._id = uuid.uuid1()
        self.output_file_name = self._id.hex
