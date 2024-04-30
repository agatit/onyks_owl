from label_selector.LabelSelector import LabelSelector


def check_saves(app: LabelSelector, target: str, *trace_args) -> None:
    checkpoints = app.save_manager.get_checkpoints()

    for checkpoint in checkpoints:
        if app.total_changed_index % checkpoint.period == 0:
            app.save_checkpoint(checkpoint.name)

            if not checkpoint.silent:
                top_bar = app.nametowidget(target)
                top_bar.set_info_with_timer("Auto saved", 2000)
