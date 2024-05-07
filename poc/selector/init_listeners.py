from functools import partial

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.listeners.ChangeImageBrightness import change_image_brightness
from selector.listeners.CheckSaves import check_saves
from selector.listeners.LoadCheckpoint import load_checkpoint
from selector.listeners.ReloadCounter import reload_counter
from selector.listeners.ReloadImage import reload_image
from selector.listeners.ReloadImageName import reload_image_name
from selector.listeners.ReloadLabel import reload_label
from selector.listeners.ReloadResultsListbox import reload_results_listbox
from selector.listeners.UnselectLabelRectangles import unselect_label_rectangles
from selector.listeners.UpdateLabelText import update_label_text
from selector.listeners.UpdateTotalChangedIndex import update_total_changed_index


def init_default_listeners(app: Selector, model: SelectorModel):
    mainwindow_str = "!mainwindow"
    topbar_str = "!mainwindow.!topbar"
    scale_str = "!mainwindow.sidebar.!scalewithlabel"
    results_listbox_str = "!mainwindow.sidebar.results_listbox"

    app.current_index_var.trace("w", partial(check_saves, app, model, topbar_str))
    app.current_index_var.trace("w", partial(reload_results_listbox, app, model, results_listbox_str))
    app.current_index_var.trace("w", partial(reload_counter, app, model, topbar_str))
    app.current_index_var.trace("w", partial(reload_image_name, app, model, topbar_str))
    app.current_index_var.trace("w", partial(reload_image, app, model, mainwindow_str))
    app.current_index_var.trace("w", partial(unselect_label_rectangles, app, model, None))
    app.current_index_var.trace("w", partial(update_total_changed_index, app, model, None))

    brightness_var = app.nametowidget(scale_str).scale_var
    brightness_var.trace("w", partial(change_image_brightness, app, model, scale_str))

    app.current_label_id_var.trace("w", partial(reload_label, app, model, topbar_str))
    app.current_label_id_var.trace("w", partial(update_label_text, app, model, None))

    reload_main_window_callbacks: list = [
        partial(reload_image, app, model, mainwindow_str),
        partial(reload_image_name, app, model, topbar_str),
        partial(reload_counter, app, model, topbar_str),
        partial(reload_label, app, model, topbar_str),
        partial(update_label_text, app, model, None),
        partial(reload_results_listbox, app, model, results_listbox_str)
    ]

    app.add_listener("reload_main_window", partial(reload_main_window, *reload_main_window_callbacks))
    app.add_listener("reload_image", partial(reload_image, app, model, mainwindow_str))
    app.add_listener("reload_results_listbox", partial(reload_results_listbox, app, model, results_listbox_str))
    app.add_listener("load_checkpoint", partial(load_checkpoint, app, model, None))

    app.notify_listener("reload_main_window")


def reload_main_window(*reload_callbacks) -> None:
    for callback in reload_callbacks:
        callback()
