from selector.Selector import Selector


def reload_image(app: Selector, target: str, *trace_args) -> None:
    current_process_data = app.get_current_process_data()

    current_image = current_process_data.image_path
    label_rectangles = current_process_data.label_rectangles

    main_window = app.nametowidget(target)
    main_window.load_image(current_image, label_rectangles)
