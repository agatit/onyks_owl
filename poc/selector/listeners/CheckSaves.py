from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def check_saves(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    checkpoints = model.save_manager.get_checkpoints()

    for checkpoint in checkpoints:
        if app.total_changed_index % checkpoint.period == 0:
            current_index = app.current_index_var.get()
            model.save_checkpoint(checkpoint.name, current_index)

            if not checkpoint.silent:
                top_bar = app.nametowidget(target)
                top_bar.set_info_with_timer("Auto saved", 2000)
