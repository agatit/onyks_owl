import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class ListBoxSelectLabelCommand(Command):
    listbox: tkinter.Listbox

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_indexes = self.listbox.curselection()

        if len(selected_indexes) > 0:
            self.app.current_label_id_var.set(selected_indexes[0])

        return True

    def undo(self) -> None:
        pass
