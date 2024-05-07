from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def update_label_text(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    label_id = app.current_label_id_var.get()
    app.current_label_text = model.labels[label_id]
