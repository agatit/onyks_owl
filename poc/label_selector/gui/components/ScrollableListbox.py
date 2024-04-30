import tkinter as tk


class ScrollableListbox(tk.Frame):

    def __init__(self, parent, title: str, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        title_label = tk.Label(self, text=title, width=10, anchor=tk.N)
        title_label.pack(side=tk.TOP, expand=False, anchor=tk.N, fill=tk.X)
        self.title_label = title_label

        listbox_container = tk.Frame(self, name="listbox_container")
        listbox_container.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH)
        self.listbox_container = listbox_container

        scrollbar = tk.Scrollbar(listbox_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar = scrollbar

        self.listbox_var = tk.StringVar(self, None)
        listbox = tk.Listbox(listbox_container, listvariable=self.listbox_var, yscrollcommand=scrollbar.set, width=30)
        listbox.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH)
        self.listbox = listbox

        scrollbar.config(command=listbox.yview)

