from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def reload_results_listbox(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    current_data = model.get_data(app.current_index_var.get())
    rectangles = current_data.label_rectangles
    _list = [f"{label_rectangle.label_text}({i})" for i, label_rectangle in enumerate(rectangles)]

    listbox = app.nametowidget(target)
    listbox.listbox_var.set(_list)
