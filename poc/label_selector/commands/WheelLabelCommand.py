import tkinter

from label_selector.commands.Command import Command


class WheelLabelCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app

        labels_number = len(app.labels)
        current_id = app.current_label_id

        if event.delta > 0:
            next_id = current_id + 1
        else:
            next_id = current_id - 1

        if next_id < 0:
            next_id = labels_number - 1
        elif next_id >= labels_number:
            next_id = 0

        app.current_label_id = next_id
        app.current_label_text = app.labels[next_id]

        app.reload_label()
        return True

    def undo(self) -> None:
        pass
