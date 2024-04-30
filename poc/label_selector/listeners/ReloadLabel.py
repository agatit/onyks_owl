from label_selector.LabelSelector import LabelSelector
from label_selector.gui.components.TopBar import TopBarLabels


def reload_label(app: LabelSelector, target: str, *trace_args) -> None:
    top_bar = app.nametowidget(target)
    top_bar.set_label(TopBarLabels.ClASS, app.current_label_text)
