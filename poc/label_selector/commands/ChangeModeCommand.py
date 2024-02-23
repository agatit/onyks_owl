import tkinter
from dataclasses import field, dataclass

from label_selector.commands.Command import Command


@dataclass
class ChangeModeCommand(Command):
    mode_str: str
    last_mode_str: str = field(init=False, repr=False)

    def execute(self, event: tkinter.Event = None) -> bool:
        self.last_mode_str = self.app.get_current_mode()
        self.app.activate_mode(self.mode_str)
        return True

    def undo(self) -> None:
        self.app.activate_mode(self.last_mode_str)
