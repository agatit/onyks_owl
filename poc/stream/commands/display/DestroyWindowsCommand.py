import cv2

from stream.commands.Command import Command


class DestroyWindowsCommand(Command):
    def execute(self) -> None:
        cv2.destroyAllWindows()
