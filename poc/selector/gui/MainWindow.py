import tkinter as tk


class MainWindow(tk.Frame):
    START_POINT_THICKNESS: int = 4

    def __init__(self, parent: tk.Tk, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

