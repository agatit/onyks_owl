import tkinter as tk
from enum import Enum, auto
from functools import partial


class TopBarLabels(str, Enum):
    INFO = auto()
    ClASS = auto()
    IMAGE = auto()
    COUNTER = auto()


class TopBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        info_label_text = tk.StringVar(self, name=TopBarLabels.INFO)
        info_label = tk.Label(self, textvariable=info_label_text, width=10, anchor=tk.W)
        info_label.pack(side=tk.LEFT, expand=False)
        info_label_text.trace("w", partial(self._update_label, label=info_label))
        self.info_label = info_label

        class_label_text = tk.StringVar(self, value="class", name=TopBarLabels.ClASS)
        class_label = tk.Label(self, textvariable=class_label_text, text="class", width=30)
        class_label.pack(side=tk.LEFT, expand=True)
        info_label_text.trace("w", partial(self._update_label, label=class_label))
        self.class_label = class_label

        image_name_text = tk.StringVar(self, value="Image", name=TopBarLabels.IMAGE)
        image_name = tk.Label(self, textvariable=image_name_text, width=40)
        image_name.pack(side=tk.LEFT, expand=True)
        info_label_text.trace("w", partial(self._update_label, label=image_name))
        self.image_name = image_name

        counter_label_text = tk.StringVar(value="counter", name=TopBarLabels.COUNTER)
        counter_label = tk.Label(self, textvariable=counter_label_text, width=10, anchor=tk.E)
        counter_label.pack(side=tk.LEFT, expand=False)
        info_label_text.trace("w", partial(self._update_label, label=counter_label))
        self.counter_label = counter_label

    def _update_label(self, label: tk.Label, top_bar_label_value: str, *args):
        var = TopBarLabels(top_bar_label_value)
        label.config(text=self.getvar(var))

    def set_label(self, top_bar_label: TopBarLabels, value: str):
        self.setvar(name=top_bar_label, value=value)

    def set_counter(self, current: int, max_number: int) -> None:
        text = f"{current + 1}/{max_number}"
        self.setvar(TopBarLabels.COUNTER, text)

    def set_info_with_timer(self, text: str, delay_ms: int) -> None:
        self.set_label(TopBarLabels.INFO, text)
        self.after(delay_ms, lambda: self.set_label(TopBarLabels.INFO, ''))
