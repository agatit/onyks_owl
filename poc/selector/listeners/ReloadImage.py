from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def reload_image(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    current_process_data = model.get_data(app.current_index_var.get())

    current_image = current_process_data.image_path
    label_rectangles = current_process_data.label_rectangles

    main_window = app.nametowidget(target)
    main_window.load_image(current_image, label_rectangles)
