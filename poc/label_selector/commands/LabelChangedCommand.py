import tkinter

from label_selector.commands.Command import Command


class LabelChangedCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        pass

    def undo(self) -> None:
        pass