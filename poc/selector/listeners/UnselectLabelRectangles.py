from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def unselect_label_rectangles(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    current_process_data = model.get_data(app.current_index_var.get())

    for label_rectangle in current_process_data.label_rectangles:
        label_rectangle.selected = False
