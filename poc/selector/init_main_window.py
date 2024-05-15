import tkinter as tk

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.MainWindow import MainWindow
from selector.gui.components.ImageCanvas import ImageCanvas
from selector.gui.components.ScaleWithLabel import ScaleWithLabel
from selector.gui.components.ScrollableListbox import ScrollableListbox
from selector.gui.components.TopBar import TopBar


def init_default_main_window(app: Selector, model: SelectorModel):
    app.geometry('800x600')

    main_window = MainWindow(app)
    main_window.pack(anchor="center", fill="both", expand=True)
    app.main_window = main_window

    top_bar = TopBar(main_window)
    top_bar.pack(side=tk.TOP, fill=tk.X)

    image_canvas = ImageCanvas(main_window, bg="grey")
    image_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    side_bar = tk.Frame(app.main_window, name="sidebar")
    side_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    scale_with_label = ScaleWithLabel(side_bar, "Brightness")
    scale_with_label.pack(side=tk.TOP, expand=False, anchor=tk.N)

