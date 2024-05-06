import tkinter as tk


class ScaleWithLabel(tk.Frame):

    def __init__(self, parent, label_text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        label = tk.Label(self, text=label_text, width=10, anchor=tk.N)
        label.pack(side=tk.TOP, expand=False, anchor=tk.N)
        self.info_label = label

        self.scale_var = tk.IntVar(self, value=100, name="scale_var")
        scale = tk.Scale(self, variable=self.scale_var, orient=tk.HORIZONTAL, length=200, from_=100, to=1000)
        scale.pack(side=tk.TOP, expand=False, anchor=tk.N)
        self.scale = scale
