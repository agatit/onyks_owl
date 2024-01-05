from dataclasses import dataclass, field
from pathlib import Path

from find_frames_with_tags_scripts.OutputData import OutputData
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.DetectionResult import DetectionResult
from yolo.YoloDetector import YoloDetector


@dataclass
class ProcessData:
    movie_path: Path
    output_dir: Path
    output_extension: str
    rectifier: FrameRectifier
    model: YoloDetector
    labels: list[str]
    output_data: list[OutputData] = field(init=False, default_factory=list)
