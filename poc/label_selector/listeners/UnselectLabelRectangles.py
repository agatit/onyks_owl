from label_selector.LabelSelector import LabelSelector


def unselect_label_rectangles(app: LabelSelector, target: str, *trace_args) -> None:
    current_process_data = app.get_current_process_data()

    for label_rectangle in current_process_data.label_rectangles:
        label_rectangle.selected = False
