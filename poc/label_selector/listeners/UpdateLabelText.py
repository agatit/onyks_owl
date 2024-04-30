from label_selector.LabelSelector import LabelSelector


def update_label_text(app: LabelSelector, target: str, *trace_args) -> None:
    label_id = app.current_label_id_var.get()
    app.current_label_text = app.labels[label_id]
