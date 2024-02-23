import copy
from dataclasses import dataclass, field
from itertools import compress
from typing import Type, Any

from label_selector.commands.Command import Command


@dataclass
class ChainCommand(Command):
    commands_types: list[type, list[Any]] = field(repr=False)

    commands: list[Command] = field(init=False, repr=False, default_factory=list)
    results: list[bool] = field(init=False, repr=False)

    def execute(self, event=None) -> bool:
        self.commands = [_type(*args) for _type, args in self.commands_types]
        self.results = [i.execute(event) for i in self.commands]

        return any(self.results)

    def undo(self) -> None:
        true_commands = compress(self.commands, self.results)
        for command in true_commands:
            command.undo()
