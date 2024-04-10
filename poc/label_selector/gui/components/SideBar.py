import tkinter as tk

from label_selector.gui.components.ScrollableListbox import ScrollableListbox


class SideBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        info_label = tk.Label(self, text="Brightness", width=10, anchor=tk.N)
        info_label.pack(side=tk.TOP, expand=False, anchor=tk.N)
        self.info_label = info_label

        self.gamma_value = tk.IntVar(value=100)
        gamma_scale = tk.Scale(self, variable=self.gamma_value, orient=tk.HORIZONTAL, length=200, from_=100, to=500)
        gamma_scale.pack(side=tk.TOP, expand=False, anchor=tk.N)
        self.gamma_scale = gamma_scale

        self.classes_listbox = ScrollableListbox(self, "Classes")
        self.classes_listbox.listbox.config(selectmode='browse')
        self.classes_listbox.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH)

        self.results_listbox = ScrollableListbox(self, "Results")
        self.results_listbox.listbox.config(selectmode='extended')
        self.results_listbox.pack(side=tk.TOP, expand=True, anchor=tk.S, fill=tk.BOTH)

        self.remove_button = tk.Button(self.results_listbox, text="Remove")
        self.remove_button.pack(fill=tk.X)

        # for i in range(100):
        #     self.classes_listbox.listbox.insert("end", i)
        #     self.results_listbox.listbox.insert("end", i)

