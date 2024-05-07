from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def load_checkpoint(app: Selector, model: SelectorModel, target: str, *trace_args) -> None:
    checkpoint = model.save_manager.get_latest_checkpoint()

    if checkpoint is not None:
        data = checkpoint.load()

        model.to_export = data[0]
        model.process_data = data[2]

        app.current_index_var.set(data[1])
        app.notify_listener("reload_main_window")
