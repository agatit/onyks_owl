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
from selector.tracing.TraceRegister import trace_add


def init_default_listeners(app: Selector, model: SelectorModel):
    mainwindow_str = "!mainwindow"
    topbar_str = "!mainwindow.!topbar"
    scale_str = "!mainwindow.sidebar.!scalewithlabel"

    app.var_register.add_var("brightness_var", app.nametowidget(scale_str).scale_var)

    index_var = "current_index_var"
    label_var = "current_label_id_var"
    scale_var = "brightness_var"

    index_var_write = partial(
        trace_add,
        register=app.var_register,
        var_name=index_var,
        mode="write"
    )
    index_var_write(
        trace_name="check_saves",
        callback=partial(check_saves, app, model, topbar_str)
    )
    index_var_write(
        trace_name="reload_counter",
        callback=partial(reload_counter, app, model, topbar_str)
    )
    index_var_write(
        trace_name="reload_image",
        callback=partial(reload_image, app, model, mainwindow_str)
    )
    index_var_write(
        trace_name="unselect_label_rectangles",
        callback=partial(unselect_label_rectangles, app, model, None)
    )
    index_var_write(
        trace_name="update_total_changed_index",
        callback=partial(update_total_changed_index, app, model, None)
    )

    # callback =
    # app.var_register.trace_add(index_var, "write", callback)
    # callback = partial(check_saves, app, model, topbar_str)
    # app.var_register.trace_add(index_var, "write", callback)

    # aa= app.current_index_var.trace_vinfo()
    # app.current_index_var.trace_remove("write",aa_trace)
    # a = app.current_index_var.trace_vinfo()

    scale_var_write = partial(
        trace_add,
        register=app.var_register,
        var_name=scale_var,
        mode="write"
    )
    scale_var_write(
        trace_name="change_image_brightness",
        callback=partial(change_image_brightness, app, model, None)
    )
    # scale_var.trace("w", partial(change_image_brightness, app, model, scale_str))
    # scale_var.trace("w", partial(change_image_brightness, app, model, scale_str))

    label_var_write = partial(
        trace_add,
        register=app.var_register,
        var_name=label_var,
        mode="write"
    )
    label_var_write(
        trace_name="reload_label",
        callback=partial(reload_label, app, model, topbar_str)
    )
    label_var_write(
        trace_name="update_label_text",
        callback=partial(update_label_text, app, model, None)
    )

    # app.current_label_id_var.trace("w", partial(reload_label, app, model, topbar_str))
    # app.current_label_id_var.trace("w", partial(update_label_text, app, model, None))

    # reload_main_window_callbacks: list = [
    #     partial(reload_image, app, model, mainwindow_str),
    #     partial(reload_image_name, app, model, topbar_str),
    #     partial(reload_counter, app, model, topbar_str),
    #     partial(reload_label, app, model, topbar_str),
    #     partial(update_label_text, app, model, None),
    #     partial(reload_results_listbox, app, model, results_listbox_str)
    # ]

    app.add_listener("reload_image", partial(reload_image, app, model, mainwindow_str))
    # app.add_listener("reload_results_listbox", partial(reload_results_listbox, app, model, results_listbox_str))
    app.add_listener("load_checkpoint", partial(load_checkpoint, app, model, None))


def reload_main_window(*reload_callbacks) -> None:
    for callback in reload_callbacks:
        callback()
