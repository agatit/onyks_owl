import tkinter
from dataclasses import dataclass, field

from selector.commands.Command import Command
from selector.commands.listbox.ListBoxCommand import ListBoxCommand
from selector.gui.LabelRectangle import LabelRectangle


@dataclass
class RemoveLabelCommand(ListBoxCommand):
    _deleted: list[LabelRectangle] = field(init=False, default_factory=list)

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_indexes = self.listbox.curselection()
        current_process_data = self.model.get_data(self.app.current_index_var.get())

        if len(selected_indexes) < 1:
            return False

        label_rectangles = current_process_data.label_rectangles
        for index, label_rectangle in enumerate(label_rectangles):
            if index in selected_indexes:
                self._deleted.append(label_rectangle)

        current_process_data.label_rectangles = [i for i in label_rectangles
                                                 if i not in self._deleted]

        self.app.notify_listener("reload_image")
        self.app.notify_listener("reload_results_listbox")

        return True

    def undo(self) -> None:
        current_process_data = self.model.get_data(self.app.current_index_var.get())

        for deleted in self._deleted:
            current_process_data.label_rectangles.append(deleted)

        self.app.notify_listener("reload_image")
        self.app.notify_listener("reload_results_listbox")
