import cv2

from stream.commands.Command import Command


class InterruptStreamCommand(Command):
    def execute(self) -> None:
        key = cv2.waitKey(25)

        # check if window still exists
        if not cv2.getWindowProperty(self.stream.name, cv2.WND_PROP_VISIBLE):
            self.stream.active_image_gen.close()

        if key == ord('q'):
            self.stream.active_image_gen.close()
