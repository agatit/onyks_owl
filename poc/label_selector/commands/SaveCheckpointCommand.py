import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class SaveCheckpointCommand(Command):
    checkpoint_name: str

    def execute(self, event: tkinter.Event = None) -> bool:
        checkpoint = self.app.save_manager.get_checkpoint(self.checkpoint_name)

        if self.app.total_changed_index % checkpoint.period == 0:
            self.app.save_checkpoint(self.checkpoint_name)

            if not checkpoint.silent:
                self.main_window.set_info_with_timer("Auto saved", 2000)


        return True

    def undo(self) -> None:
        pass
