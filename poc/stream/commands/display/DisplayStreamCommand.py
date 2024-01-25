from dataclasses import dataclass

import cv2

from stream.commands.Command import Command

@dataclass
class DisplayStreamCommand(Command):

    def execute(self) -> None:
        cv2.imshow('Frame', self.stream.current_frame)



