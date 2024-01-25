from dataclasses import dataclass, field

from stream.commands.Command import Command


@dataclass
class CommandInvoker:
    _commands: list[Command] = field(default_factory=list)

    def add_command(self, command: Command):
        self._commands.append(command)

    def invoke(self):
        for command in self._commands:
            command.execute()
