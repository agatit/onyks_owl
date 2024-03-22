import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class ChangeLabelCommand(Command):
    class_id: int
    label: str

    def execute(self, event: tkinter.Event = None) -> bool:
        self.app.current_label_id = self.class_id
        self.app.current_label_text = self.label

        self.app.reload_label()
        return True

    def undo(self) -> None:
        pass
