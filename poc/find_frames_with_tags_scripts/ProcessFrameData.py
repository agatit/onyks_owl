from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Callable

import numpy as np

from find_frames_with_tags_scripts.FindFramesWithTagsData import FindFramesWithTagsData
from find_frames_with_tags_scripts.filtering.batch_filtering import BatchFilterCallback
from find_frames_with_tags_scripts.filtering.detecions_filtering import DetectionsFilterCallback
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.DetectionResult import DetectionResult
from yolo.yolo_detectors.YoloDetector import YoloDetector


ExportFrameCallback = Callable[[np.ndarray], None]
ExportFrameWithDetectionsCallback = Callable[[np.ndarray, Iterable[DetectionResult]], None]



def _empty(*args, **kwargs):
    pass


@dataclass
class ProcessFrameData:
    movie_path: Path
    output_dir: Path
    output_extension: str

    rectifier: FrameRectifier
    model: YoloDetector
    empty_image_step: int

    batch_filter_callbacks: list[BatchFilterCallback] = field(init=False, default_factory=list)
    detections_filter_callbacks: list[DetectionsFilterCallback] = field(init=False, default_factory=list)
    export_frame_callbacks: list[ExportFrameCallback] = field(init=False, default_factory=list)
    export_frame_with_detections_callbacks: list[ExportFrameWithDetectionsCallback] = field(init=False,
                                                                                            default_factory=list)
    output_data: list[FindFramesWithTagsData] = field(init=False, default_factory=list)
    export_frame_counter: int = field(init=False, default=0)

    BOUNDING_BOX_FILE_SUFFIX = "_b"

    def append_output_data(self, detection_results: Iterable[DetectionResult]):
        extension = self.output_extension
        counter = self.export_frame_counter

        if len(detection_results) < 1:
            file_name = str(counter) + extension

            output_data = FindFramesWithTagsData(counter, file_name)
            self.output_data.append(output_data)

        for index, detection_result in enumerate(detection_results):
            name = detection_result.class_name
            file_name = f"{counter}_{name}_{index}" + extension

            output_data = FindFramesWithTagsData(counter, file_name, detection_result)
            self.output_data.append(output_data)

    def update_export_frame_counter(self):
        self.export_frame_counter += 1

    def rectify_frame(self, frame: np.ndarray) -> np.ndarray:
        if self.rectifier:
            return self.rectifier.rectify(frame)
        else:
            return frame

    def filter_batch(self, batch: Iterable[np.ndarray]) -> list[np.ndarray]:
        for batch_filter in self.batch_filter_callbacks:
            batch = batch_filter(batch)

        return batch

    def check_detections(self, detections: Iterable[DetectionResult]) -> bool:
        results = []

        for detection_filter in self.detections_filter_callbacks:
            result = detection_filter(detections)
            results.append(result)

        return all(results)

    def export_frame(self, frame: np.ndarray) -> None:
        for frame_exporter in self.export_frame_callbacks:
            frame_exporter(frame)

    def export_frames_with_detections(self, frame: np.ndarray, detections: Iterable[DetectionResult]) -> None:
        for frame_exporter in self.export_frame_with_detections_callbacks:
            frame_exporter(frame, detections)


