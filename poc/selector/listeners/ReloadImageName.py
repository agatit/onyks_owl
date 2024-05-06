from selector.Selector import Selector
from selector.gui.components.TopBar import TopBarLabels


def reload_image_name(app: Selector, target: str, *trace_args) -> None:
    name = app.get_current_process_data().image_path.name
    top_bar = app.nametowidget(target)
    top_bar.set_label(TopBarLabels.IMAGE, name)
