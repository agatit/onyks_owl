from dataclasses import dataclass, field
from typing import Generator

import numpy as np

from stitch.rectify.FrameRectifier import FrameRectifier
from stream.loaders.Loader import Loader
from yolo.DetectionResult import DetectionResult
from yolo.YoloDetector import YoloDetector


@dataclass
class Stream:
    loader: Loader = None
    frame_rectifier: FrameRectifier = None
    yolo_detector: YoloDetector = None

    current_frame: np.ndarray = field(init=False)
    active_image_gen: Generator[np.ndarray, None, np.ndarray] = field(init=False)
    detections: list[list[DetectionResult]] = field(init=False, default_factory=list)
    read_frames_counter: int = 0

    def __post_init__(self):
        self.reload_image_generator()

    def get_next_frame_gen(self) -> np.ndarray:
        for frame in self.active_image_gen:
            self.current_frame = frame
            self.read_frames_counter += 1
            yield

    def reload_image_generator(self):
        self.active_image_gen = self.loader.get_image_gen()
