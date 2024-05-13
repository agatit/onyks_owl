from dataclasses import dataclass, field

from select_frames_with_tags_test.test_filter_output_json import DetectionResult
from stream.Stream import Stream
from yolo.yolo_detectors.YoloDetectorV5 import YoloDetectorV5


@dataclass(kw_only=True)
class YoloStream(Stream):
    yolo_detector: YoloDetectorV5 = None
    detections: list[list[DetectionResult]] = field(init=False, default_factory=list)
