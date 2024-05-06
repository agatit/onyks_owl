import tkinter

from selector.commands.Command import Command


class NextLabelCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app

        next_id = app.current_label_id_var.get() + 1
        if next_id >= len(app.labels):
            next_id = 0

        app.current_label_id_var.set(next_id)
        return True

    def undo(self) -> None:
        pass
