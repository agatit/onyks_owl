from stream.commands.Command import Command


class DrawBoundingBoxesCommand(Command):
    def execute(self) -> None:
        last_results = self.stream.detections[-1]
        frame = self.stream.current_frame

        for result in last_results[0]:
            self.stream.current_frame = result.draw_on_image(frame)

