from dataclasses import dataclass, field
from typing import Any, Callable

from label_selector.commands.Command import Command


@dataclass
class ToggleCommand(Command):
    flag_callback: Callable[[], bool] = field(repr=False)
    on_true_command: list[type, list[Any]] = field(repr=False)
    on_false_command: list[type, list[Any]] = field(repr=False)

    selected: Command = field(init=False, repr=False)

    def execute(self, event=None) -> bool:

        if self.flag_callback():
            _class = self.on_true_command[0]
            args = self.on_true_command[1]
        else:
            _class = self.on_false_command[0]
            args = self.on_false_command[1]

        self.selected = _class(*args)
        self.selected.execute(event)
        return True

    def undo(self) -> None:
        self.selected.undo()
