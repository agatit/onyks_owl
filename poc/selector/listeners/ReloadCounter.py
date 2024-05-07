from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def reload_counter(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    top_bar = app.nametowidget(target)

    current_index = app.current_index_var.get()
    max_index = model.get_data_len()

    top_bar.set_counter(current_index, max_index)
