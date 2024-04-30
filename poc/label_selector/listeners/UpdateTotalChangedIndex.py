from label_selector.LabelSelector import LabelSelector


def update_total_changed_index(app: LabelSelector, target: str, *trace_args) -> None:
    app.total_changed_index += 1
