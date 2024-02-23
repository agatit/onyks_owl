import tkinter

from label_selector.commands.Command import Command


class NextLabelCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app

        app.selected_label_id = next(app.labels_id_cycle)
        app.selected_label_text = next(app.labels_text_cycle)

        app.reload_label()
        return True

    def undo(self) -> None:
        pass
