import tkinter
from dataclasses import dataclass, field
from typing import ClassVar

from label_selector.commands.Command import Command


@dataclass
class ListBoxGlowSelectedLabelCommand(Command):
    listbox: tkinter.Listbox

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_indexes = self.listbox.curselection()
        current_process_data = self.app.get_current_process_data()

        for index, label_rectangle in enumerate(current_process_data.label_rectangles):
            if index in selected_indexes:
                label_rectangle.selected = True
            else:
                label_rectangle.selected = False

        self.app.notify_listener("reload_image")

        return True

    def undo(self) -> None:
        pass
