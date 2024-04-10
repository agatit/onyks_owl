import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class ListBoxSelectLabelCommand(Command):
    listbox: tkinter.Listbox

    def execute(self, event: tkinter.Event = None) -> bool:
        pass

    def undo(self) -> None:
        pass
