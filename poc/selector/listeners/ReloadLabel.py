from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.TopBar import TopBarLabels


def reload_label(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    top_bar = app.nametowidget(target)
    top_bar.set_label(TopBarLabels.ClASS, app.current_label_text)
