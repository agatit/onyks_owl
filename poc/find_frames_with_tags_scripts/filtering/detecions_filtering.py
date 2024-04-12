from typing import Callable, Iterable

from yolo.DetectionResult import DetectionResult

FilterFun = Callable[[DetectionResult], bool]
DetectionsFilterCallback = Callable[[Iterable[DetectionResult]], bool]


def any_below_threshold_filter(detections: Iterable[DetectionResult], upper_threshold: float = 0.7) -> bool:
    return any(detection.confidence < upper_threshold for detection in detections)


