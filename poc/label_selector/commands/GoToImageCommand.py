import tkinter
from dataclasses import dataclass, field

from label_selector.commands.Command import Command


@dataclass
class GoToImageCommand(Command):
    go_to_index: int
    last_index: int = field(init=False, default=0)

    def execute(self, event: tkinter.Event = None) -> bool:
        self.last_index = self.app.current_index

        self.app.current_index = self.go_to_index
        self.app.reload_main_window()

    def undo(self) -> None:
        self.app.current_index = self.last_index
        self.app.reload_main_window()
