import tkinter
from dataclasses import dataclass, field

from selector.commands.Command import Command


@dataclass
class GoToImageCommand(Command):
    go_to_index: int
    last_index: int = field(init=False, default=0)

    def execute(self, event: tkinter.Event = None) -> bool:
        self.last_index = self.app.current_index_var.get()
        self.app.current_index_var.set(self.go_to_index)


    def undo(self) -> None:
        self.app.current_index_var.set(self.last_index)
