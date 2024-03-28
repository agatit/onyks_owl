import tkinter

from label_selector.commands.Command import Command


class SavePeriodicCheckpointCommand(Command):
    silent: bool = False
    period: int = 10

    def execute(self, event: tkinter.Event = None) -> bool:

        if self.app.total_changed_index % self.period == 0:
            self.app.save_checkpoint(self.app.periodic_checkpoint_name)

            if not self.silent:
                self.main_window.set_info_with_timer("Auto saved", 2000)

        return True

    def undo(self) -> None:
        pass
