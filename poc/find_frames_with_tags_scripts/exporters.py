from typing import Iterable

import cv2
import numpy as np

from find_frames_with_tags_scripts.ProcessFrameData import ProcessFrameData
from yolo.DetectionResult import DetectionResult


def export_original_image(process_frame_data: ProcessFrameData, frame: np.ndarray) -> None:
    frame_file_name = str(process_frame_data.export_frame_counter) + process_frame_data.output_extension
    frame_file_path = str(process_frame_data.output_dir / frame_file_name)

    cv2.imwrite(frame_file_path, frame)


def export_cropped_class(process_frame_data: ProcessFrameData, frame: np.ndarray,
                         detection_results: Iterable[DetectionResult], classes: list[int]) -> None:
    extension = process_frame_data.output_extension
    counter = process_frame_data.export_frame_counter

    for index, detection_result in enumerate(detection_results):
        if detection_result.yolo_format.class_id not in classes:
            continue

        name = detection_result.class_name
        file_name = f"{counter}_{name}_{index}" + extension
        file_path = str(process_frame_data.output_dir / file_name)

        box = detection_result.bounding_box
        cropped = frame[box.y1:box.y2, box.x1:box.x2]

        cv2.imwrite(file_path, cropped)


def export_bounding_box_image(process_frame_data: ProcessFrameData, frame: np.ndarray,
                              detection_results: Iterable[DetectionResult], classes: list[int]) -> None:
    data = process_frame_data

    frame_file_name = str(data.export_frame_counter) + data.BOUNDING_BOX_FILE_SUFFIX + data.output_extension
    frame_file_path = str(data.output_dir / frame_file_name)

    for detection_result in detection_results:
        if detection_result.yolo_format.class_id not in classes:
            continue

        frame = detection_result.draw_on_image(frame)

    cv2.imwrite(frame_file_path, frame)
