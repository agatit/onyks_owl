import tkinter
from dataclasses import dataclass, field

from label_selector.commands.listbox.ListBoxCommand import ListBoxCommand
from label_selector.gui.LabelRectangle import LabelRectangle


@dataclass
class ChangeLabelToSelectedCommand(ListBoxCommand):
    _changed: dict[int, tuple[int, str]] = field(init=False, default_factory=dict)

    def execute(self, event: tkinter.Event = None) -> bool:
        selected_indexes = self.listbox.curselection()
        current_process_data = self.app.get_current_process_data()

        if len(selected_indexes) < 1:
            return False

        current_id = self.app.current_label_id_var.get()
        current_label = self.app.current_label_text

        for index, label_rectangle in enumerate(current_process_data.label_rectangles):
            if index in selected_indexes:
                self._changed[index] = (label_rectangle.label_id, label_rectangle.label_text)

                label_rectangle.label_id = current_id
                label_rectangle.label_text = current_label
                label_rectangle.reload_full_label()

        self.app.notify_listener("reload_image")
        self.app.notify_listener("reload_results_listbox")

        return True

    def undo(self) -> None:
        current_process_data = self.app.get_current_process_data()

        for index, id_label in self._changed.items():
            _id, label = id_label
            label_rectangle = current_process_data.label_rectangles[index]

            label_rectangle.label_id = _id
            label_rectangle.label_text = label

        self.app.notify_listener("reload_image")
        self.app.notify_listener("reload_results_listbox")

