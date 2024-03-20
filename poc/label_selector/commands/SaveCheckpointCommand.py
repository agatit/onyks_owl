import tkinter
from dataclasses import dataclass

from label_selector.commands.Command import Command


@dataclass
class SaveCheckpointCommand(Command):
    silent: bool = True

    def execute(self, event: tkinter.Event = None) -> bool:
        self.app.save_checkpoint()

        if not self.silent:
            self.main_window.set_info_with_timer("Saved", 2000)

        return True

    def undo(self) -> None:
        pass
