import cv2

from stream.commands.Command import Command


class InterruptStreamCommand(Command):
    def execute(self) -> None:
        if cv2.waitKey(25) & 0xFF == ord('q'):
            self.stream.active_image_gen.close()