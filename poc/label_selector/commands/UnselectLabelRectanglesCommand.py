import tkinter

from label_selector.commands.Command import Command


class UnselectLabelRectanglesCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        current_process_data = self.app.get_current_process_data()
        for label_rectangle in current_process_data.label_rectangles:
            label_rectangle.selected = False

        self.app.notify_listener("reload_image")

        return True

    def undo(self) -> None:
        pass