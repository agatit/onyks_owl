from dataclasses import dataclass, field

from yolo.DetectionResult import DetectionResult


@dataclass
class FindFramesWithTagsData:
    frame_number: int
    file_name: str
    detection_result: DetectionResult = field(default=None)
