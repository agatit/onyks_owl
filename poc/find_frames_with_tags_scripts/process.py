from typing import Iterable

import cv2
import numpy as np

from find_frames_with_tags_scripts.ProcessFrameData import ProcessFrameData
from find_frames_with_tags_scripts.fitering import filter_batch
from yolo.DetectionResult import DetectionResult

BOUNDING_BOX_FILE_SUFFIX = "_b"


def process(process_data: ProcessFrameData) -> None:
    input_cam = cv2.VideoCapture(str(process_data.movie_path))

    batch = []
    batch_size = process_data.model.batch_size
    empty_frames = []

    counter = 0
    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:

            frame = process_data.rectify_frame_fun(frame)
            batch.append(frame)

            if counter % process_data.empty_image_step == 0:
                empty_frames.append(frame)

            if len(batch) < batch_size:
                counter += 1
                yield
                continue

            batch = process_data.filter_batch_fun(batch)
            process_frames(process_data, batch)
            process_frames(process_data, empty_frames, False)

            empty_frames = []
            batch = []
            counter += 1
            yield
        else:
            for frame in batch:
                if counter % process_data.empty_image_step == 0:
                    empty_frames.append(frame)
                counter += 1

            batch = process_data.filter_batch_fun(batch)
            process_frames(process_data, batch)
            process_frames(process_data, empty_frames, False)

            break

    input_cam.release()


def process_frames(process_data: ProcessFrameData, batch: Iterable[np.ndarray], skip_empty_frames: bool = True):
    all_results = process_data.model(batch)

    for frame, detection_results in zip(batch, all_results):
        if len(detection_results) < 1 and skip_empty_frames:
            process_data.update_export_frame_counter()
            continue

        process_data.append_output_data(detection_results)

        process_data.export_original_image_fun(frame)
        process_data.export_cropped_class_fun(detection_results, frame)
        process_data.export_bounding_box_image_fun(detection_results, frame)

        process_data.update_export_frame_counter()


def rectify_frame(process_data: ProcessFrameData, frame: np.ndarray) -> np.ndarray:
    return process_data.rectifier.rectify(frame)


def export_original_image(process_data: ProcessFrameData, frame: np.ndarray) -> None:
    frame_file_name = str(process_data.export_frame_counter) + process_data.output_extension
    frame_file_path = str(process_data.output_dir / frame_file_name)

    cv2.imwrite(frame_file_path, frame)


def export_cropped_class(process_data: ProcessFrameData, detection_results: Iterable[DetectionResult],
                         frame: np.ndarray) -> None:
    extension = process_data.output_extension
    counter = process_data.export_frame_counter

    for index, detection_result in enumerate(detection_results):
        name = detection_result.class_name
        file_name = f"{counter}_{name}_{index}" + extension
        file_path = str(process_data.output_dir / file_name)

        box = detection_result.bounding_box
        cropped = frame[box.y1:box.y2, box.x1:box.x2]

        cv2.imwrite(file_path, cropped)


def export_bounding_box_image(process_data: ProcessFrameData, detection_results: Iterable[DetectionResult],
                              frame: np.ndarray) -> None:
    frame_file_name = str(process_data.export_frame_counter) + BOUNDING_BOX_FILE_SUFFIX + process_data.output_extension
    frame_file_path = str(process_data.output_dir / frame_file_name)

    for detection_result in detection_results:
        frame = detection_result.draw_on_image(frame)

    cv2.imwrite(frame_file_path, frame)
