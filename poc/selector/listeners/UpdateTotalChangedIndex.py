from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def update_total_changed_index(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    app.total_changed_index += 1
