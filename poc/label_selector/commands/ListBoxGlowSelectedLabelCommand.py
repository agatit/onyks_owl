import tkinter
from dataclasses import dataclass, field
from typing import ClassVar

from label_selector.commands.Command import Command


@dataclass
class ListBoxGlowSelectedLabelCommand(Command):
    listbox: tkinter.Listbox

    selected_color: ClassVar[str] = "green"
    unselected_color: ClassVar[str] = "red"

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_index = self.listbox.curselection()[0]

        current_process_data = self.app.get_current_process_data()
        for label_rectangle in current_process_data.label_rectangles:
            label_rectangle.color = self.unselected_color

        selected_label_rectangle = current_process_data.label_rectangles[selected_index]
        selected_label_rectangle.color = self.selected_color

        self.app.reload_image()

        return True

    def undo(self) -> None:
        pass
