from selector.Selector import Selector


def update_total_changed_index(app: Selector, target: str, *trace_args) -> None:
    app.total_changed_index += 1
