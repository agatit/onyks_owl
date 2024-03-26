from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

import numpy as np

from find_frames_with_tags_scripts.OutputData import OutputData
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.DetectionResult import DetectionResult
from yolo.yolo_detectors.YoloDetectorV5 import YoloDetectorV5


def _empty(*args, **kwargs):
    pass


@dataclass
class ProcessFrameData:
    movie_path: Path
    output_dir: Path
    output_extension: str

    rectifier: FrameRectifier
    model: YoloDetectorV5
    empty_image_step: int

    # functions to turn on/off
    rectify_frame_fun: Callable[[np.ndarray], np.ndarray] = field(default=(lambda x: x))
    filter_batch_fun: Callable[[Iterable[np.ndarray]], Iterable[np.ndarray]] = field(default=(lambda x: x))
    export_original_image_fun: Callable[[np.ndarray], None] = field(default=_empty)
    export_cropped_class_fun: Callable[[Iterable[DetectionResult],
                                        np.ndarray], None] = field(default=_empty)
    export_bounding_box_image_fun: Callable[[Iterable[DetectionResult],
                                             np.ndarray], None] = field(default=_empty)

    output_data: list[OutputData] = field(init=False, default_factory=list)
    export_frame_counter: int = field(init=False, default=0)

    def append_output_data(self, detection_results: Iterable[DetectionResult]):
        extension = self.output_extension
        counter = self.export_frame_counter

        if len(detection_results) < 1:
            file_name = str(counter) + extension

            output_data = OutputData(counter, file_name)
            self.output_data.append(output_data)

        for index, detection_result in enumerate(detection_results):
            name = detection_result.class_name
            file_name = f"{counter}_{name}_{index}" + extension

            output_data = OutputData(counter, file_name, detection_result)
            self.output_data.append(output_data)

    def update_export_frame_counter(self):
        self.export_frame_counter += 1
