from functools import partial

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.listeners.ChangeImageBrightness import change_image_brightness
from selector.listeners.CheckSaves import check_saves
from selector.listeners.LoadCheckpoint import load_checkpoint
from selector.listeners.ReloadCounter import reload_counter
from selector.listeners.ReloadImage import reload_image
from selector.listeners.ReloadLabel import reload_label
from selector.listeners.UnselectLabelRectangles import unselect_label_rectangles
from selector.listeners.UpdateLabelText import update_label_text
from selector.listeners.UpdateTotalChangedIndex import update_total_changed_index
from selector.tracing.TraceRegister import trace_add


def init_default_listeners(app: Selector, model: SelectorModel):
    mainwindow_str = "!mainwindow"
    topbar_str = "!mainwindow.!topbar"
    image_canvas_str = "!mainwindow.!imagecanvas"

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
        callback=partial(reload_image, app, model, image_canvas_str)
    )
    index_var_write(
        trace_name="unselect_label_rectangles",
        callback=partial(unselect_label_rectangles, app, model, None)
    )
    index_var_write(
        trace_name="update_total_changed_index",
        callback=partial(update_total_changed_index, app, model, None)
    )

    scale_var_write = partial(
        trace_add,
        register=app.var_register,
        var_name=scale_var,
        mode="write"
    )
    scale_var_write(
        trace_name="change_image_brightness",
        callback=partial(change_image_brightness, app, model, image_canvas_str)
    )

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

    app.add_listener("reload_image", partial(reload_image, app, model, image_canvas_str))
    app.add_listener("load_checkpoint", partial(load_checkpoint, app, model, None))


def reload_main_window(*reload_callbacks) -> None:
    for callback in reload_callbacks:
        callback()
