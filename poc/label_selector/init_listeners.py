from functools import partial

from label_selector.LabelSelector import LabelSelector
from label_selector.gui.components.TopBar import TopBarLabels


def init_default_listeners(app: LabelSelector):
    app.current_index_var.trace("w", partial(check_saves, app))
    app.current_index_var.trace("w", partial(reload_results_listbox, app))
    app.current_index_var.trace("w", partial(reload_counter, app))
    app.current_index_var.trace("w", partial(reload_image_name, app))
    app.current_index_var.trace("w", partial(reload_image, app))
    app.current_index_var.trace("w", partial(unselect_label_rectangles, app))
    app.current_index_var.trace("w", partial(update_total_changed_index, app))

    app.current_label_id_var.trace("w", partial(reload_label, app))
    app.current_label_id_var.trace("w", partial(update_label_text, app))

    app.add_listener("reload_image", partial(reload_image, app))
    app.add_listener("reload_main_window", partial(reload_main_window, app))
    app.add_listener("reload_results_listbox", partial(reload_results_listbox, app))

    app.notify_listener("reload_main_window")


def reload_main_window(app: LabelSelector) -> None:
    reload_image(app)
    reload_image_name(app)
    reload_counter(app)
    reload_label(app)
    reload_results_listbox(app)


def update_label_text(app: LabelSelector, *trace_args) -> None:
    app.current_label_text = app.labels[app.current_label_id_var.get()]


def update_total_changed_index(app: LabelSelector, *trace_args) -> None:
    app.total_changed_index += 1


def reload_label(app: LabelSelector, *trace_args) -> None:
    app.main_window.top_bar.set_label(TopBarLabels.ClASS, app.current_label_text)


def reload_image(app: LabelSelector, *trace_args) -> None:
    current_process_data = app.get_current_process_data()

    current_image = current_process_data.image_path
    label_rectangles = current_process_data.label_rectangles

    app.main_window.load_image(current_image, label_rectangles)


def reload_image_name(app: LabelSelector, *trace_args) -> None:
    name = app.get_current_process_data().image_path.name
    app.main_window.top_bar.set_label(TopBarLabels.IMAGE, name)


def reload_counter(app: LabelSelector, *trace_args) -> None:
    app.main_window.top_bar.set_counter(app.current_index_var.get(), app.max_index)


def reload_results_listbox(app: LabelSelector, *trace_args) -> None:
    _list = [f"{label_rectangle.label_text}({i})" for i, label_rectangle
             in enumerate(app.get_current_process_data().label_rectangles)]
    app.results_listbox_var.set(_list)


def unselect_label_rectangles(app: LabelSelector, *trace_args) -> None:
    current_process_data = app.get_current_process_data()

    for label_rectangle in current_process_data.label_rectangles:
        label_rectangle.selected = False

def check_saves(app: LabelSelector, *trace_args) -> None:
    checkpoints = app.save_manager.get_checkpoints()

    for checkpoint in checkpoints:
        if app.total_changed_index % checkpoint.period == 0:
            app.save_checkpoint(checkpoint.name)

            if not checkpoint.silent:
                app.main_window.set_info_with_timer("Auto saved", 2000)
