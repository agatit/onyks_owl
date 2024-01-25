from dataclasses import dataclass

from display.utils import scale_image_by_percent
from stream.commands.Command import Command


@dataclass
class ScaleImageCommand(Command):
    scale_percent: int = 60

    def execute(self) -> None:
        frame = self.stream.current_frame
        self.stream.current_frame = scale_image_by_percent(frame, self.scale_percent)
