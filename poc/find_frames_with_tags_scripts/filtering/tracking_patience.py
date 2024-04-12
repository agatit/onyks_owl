from dataclasses import dataclass, field
from typing import Iterable

from yolo.DetectionResult import DetectionResult


@dataclass
class PatienceTracker:
    available_classes: list[int]
    patience: int

    id_occurrence: dict[int, int] = field(default_factory=dict, init=False)

    def update_ids(self, tracked_classes: dict[int, int]) -> None:
        available_classes = self.available_classes
        known_ids = self.id_occurrence

        for new_id, _class in tracked_classes.items():
            if _class not in available_classes:
                continue

            if new_id not in known_ids.keys():
                known_ids[new_id] = 0
                continue

            known_ids[new_id] += 1

    def check_patience(self) -> list[int]:
        results = []

        for _id, occurrence in self.id_occurrence.items():
            if occurrence < self.patience:
                results.append(_id)
            else:
                self.id_occurrence[_id] = 0

        return results


def tracking_patience(detections: Iterable[DetectionResult], patience_tracker: PatienceTracker) -> bool:
    tracking_ids = {i.track_id: i.yolo_format.class_id for i in detections}
    patience_tracker.update_ids(tracking_ids)

    return len(patience_tracker.check_patience()) > 0
