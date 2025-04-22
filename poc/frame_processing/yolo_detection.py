import numpy as np

from yolo.yolo_detectors.YoloDetector import YoloDetector


def detect_batch_frames(batch: list[np.ndarray], detector: YoloDetector) -> np.ndarray:
    results = detector(batch)
    frames = []

    for frame, result in zip(batch, results):
        for detection_result in result:
            frame = detection_result.draw_on_image(frame)
            frames.append(frame)

    return frames
