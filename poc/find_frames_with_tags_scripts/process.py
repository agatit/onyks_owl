from typing import Iterable

import cv2
import numpy as np

from find_frames_with_tags_scripts.ProcessFrameData import ProcessFrameData


def process(process_data: ProcessFrameData) -> None:
    input_cam = cv2.VideoCapture(str(process_data.movie_path))

    batch = []
    batch_size = process_data.model.batch_size
    empty_frames = []

    counter = 0
    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:

            frame = process_data.rectify_frame(frame)
            batch.append(frame)

            if counter % process_data.empty_image_step == 0:
                empty_frames.append(frame)

            if len(batch) < batch_size:
                counter += 1
                yield
                continue

            batch = process_data.filter_batch(batch)
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

            batch = process_data.filter_batch(batch)
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

        if not process_data.check_detections(detection_results):
            continue

        process_data.append_output_data(detection_results)

        process_data.export_frame(frame)
        process_data.export_frames_with_detections(frame, detection_results)

        process_data.update_export_frame_counter()
