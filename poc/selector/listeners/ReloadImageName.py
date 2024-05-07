from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.TopBar import TopBarLabels


def reload_image_name(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    current_data = model.get_data(app.current_index_var.get())
    name = current_data.image_path.name

    top_bar = app.nametowidget(target)
    top_bar.set_label(TopBarLabels.IMAGE, name)
