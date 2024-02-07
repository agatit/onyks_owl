from dataclasses import dataclass

import cv2

from stream.commands.Command import Command


@dataclass
class DisplayImageCommand(Command):
    def execute(self) -> None:
        cv2.imshow(self.stream.name, self.stream.current_frame)
        cv2.waitKey(0)
