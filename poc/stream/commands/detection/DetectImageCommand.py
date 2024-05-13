from dataclasses import dataclass, field

from stream.commands.YoloCommand import YoloCommand


@dataclass
class DetectImageCommand(YoloCommand):
    labels_to_detect: list[str] = field(default_factory=list)

    def execute(self) -> None:
        frame = self.stream.current_frame

        detection_result = self.stream.yolo_detector(frame)
        self.stream.detections.append(detection_result)
