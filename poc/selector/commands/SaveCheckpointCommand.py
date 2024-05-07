import tkinter
from dataclasses import dataclass

from selector.commands.Command import Command


@dataclass
class SaveCheckpointCommand(Command):
    checkpoint_name: str

    def execute(self, event: tkinter.Event = None) -> bool:
        checkpoint = self.model.save_manager.get_checkpoint(self.checkpoint_name)

        if self.app.total_changed_index % checkpoint.period == 0:
            current_index = self.app.current_index_var.get()
            self.model.save_checkpoint(checkpoint.name, current_index)

            if not checkpoint.silent:
                #todo: przenieść na zewnątrz
                top_bar = self.app.nametowidget("!mainwindow.!topbar")
                top_bar.set_info_with_timer("Auto saved", 2000)

        return True

    def undo(self) -> None:
        pass
