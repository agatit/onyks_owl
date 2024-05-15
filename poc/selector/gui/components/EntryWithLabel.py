import tkinter as tk
from dataclasses import dataclass


class EntryWithLabel(tk.Frame):
    def __init__(self, parent, label_text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT)

        self.entry_var = tk.StringVar(self)
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
