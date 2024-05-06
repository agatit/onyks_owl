from selector.Selector import Selector


def reload_results_listbox(app: Selector, target: str, *trace_args) -> None:
    rectangles = app.get_current_process_data().label_rectangles
    _list = [f"{label_rectangle.label_text}({i})" for i, label_rectangle in enumerate(rectangles)]

    listbox = app.nametowidget(target)
    listbox.listbox_var.set(_list)
