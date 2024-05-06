from selector.Selector import Selector


def reload_counter(app: Selector, target: str, *trace_args) -> None:
    top_bar = app.nametowidget(target)
    top_bar.set_counter(app.current_index_var.get(), app.max_index)
