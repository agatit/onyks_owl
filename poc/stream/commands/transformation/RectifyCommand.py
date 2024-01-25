from dataclasses import dataclass

from stream.commands.Command import Command


@dataclass
class RectifyCommand(Command):

    def execute(self) -> None:
        frame = self.stream.current_frame
        self.stream.current_frame = self.stream.frame_rectifier.rectify(frame)

