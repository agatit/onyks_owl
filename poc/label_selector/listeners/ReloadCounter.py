from label_selector.LabelSelector import LabelSelector


def reload_counter(app: LabelSelector, target: str, *trace_args) -> None:
    top_bar = app.nametowidget(target)
    top_bar.set_counter(app.current_index_var.get(), app.max_index)
