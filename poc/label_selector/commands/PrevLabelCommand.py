import tkinter

from label_selector.commands.Command import Command


class PrevLabelCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app

        next_id = app.current_label_id - 1
        if next_id < 0:
            next_id = len(app.labels) - 1

        app.current_label_id = next_id
        app.current_label_text = app.labels[next_id]

        app.reload_label()
        return True

    def undo(self) -> None:
        pass