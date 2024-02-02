from dataclasses import field, dataclass

from select_frames_with_tags_scripts.commands.Command import Command


@dataclass
class CommandHistory:
    __commands: list[Command] = field(default_factory=list)

    def push(self, command: Command):
        self.__commands.append(command)

    def pop(self) -> Command:
        return self.__commands.pop()
