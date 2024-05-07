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

    classes_listbox = ScrollableListbox(side_bar, "Classes", name="class_listbox")
    classes_listbox.listbox.config(selectmode='browse')
    classes_listbox.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH)
    classes_listbox.listbox_var.set(list(model.labels.values()))

    results_listbox = ScrollableListbox(side_bar, "Results", name="results_listbox")
    results_listbox.listbox.config(selectmode='extended')
    results_listbox.pack(side=tk.TOP, expand=True, anchor=tk.S, fill=tk.BOTH)

    remove_button = tk.Button(results_listbox, text="Remove", name="remove_button")
    remove_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

    change_results_button = tk.Button(results_listbox, text="Change", name="change_button")
    change_results_button.pack(side=tk.RIGHT, expand=True, fill=tk.X)
