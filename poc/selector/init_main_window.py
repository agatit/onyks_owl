import tkinter as tk

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.MainWindow import MainWindow
from selector.gui.components.ScaleWithLabel import ScaleWithLabel
from selector.gui.components.ScrollableListbox import ScrollableListbox
from selector.gui.components.TopBar import TopBar


def init_default_main_window(app: Selector, model: SelectorModel):
    app.geometry('800x600')
    app.main_window = MainWindow(app)
    app.main_window.pack(anchor="center", fill="both", expand=True)

    top_bar = TopBar(app.main_window)
    top_bar.pack(side=tk.TOP, fill=tk.X)

    image_canvas = tk.Canvas(app.main_window, bg="grey")
    image_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    app.main_window.set_image_canvas(image_canvas)

    # sidebar
    side_bar = tk.Frame(app.main_window, name="sidebar")
    side_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    scale_with_label = ScaleWithLabel(side_bar, "Brightness")
    scale_with_label.pack(side=tk.TOP, expand=False, anchor=tk.N)

