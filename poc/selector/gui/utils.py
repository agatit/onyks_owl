import functools
import tkinter as tk
from typing import Callable


def open_loading_screen(fun: Callable):
    @functools.wraps(fun)
    def wrapper(parent: tk.Tk | tk.Frame, *args, **kwargs):
        top_level = tk.Toplevel()
        top_level.title("loading")

        top_level.label = tk.Label(top_level, text="Loading...")
        top_level.label.pack()

        top_level.update()
        result = fun(parent, *args, **kwargs)
        top_level.destroy()

        parent.deiconify()

        return result

    return wrapper
