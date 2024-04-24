import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class ListBoxSelectLabelCommand(Command):
    listbox: tkinter.Listbox

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_index = self.listbox.curselection()
        self.app.current_label_id = selected_index[0]

        self.app.reload_label()
        return True

    def undo(self) -> None:
        pass
