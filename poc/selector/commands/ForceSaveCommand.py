import tkinter

from selector.commands.Command import Command


class ForceSaveCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        checkpoint = self.model.save_manager.get_latest_checkpoint()

        if checkpoint is not None:
            current_index = self.app.current_index_var.get()
            self.model.save_checkpoint(checkpoint.name, current_index)

    def undo(self) -> None:
        pass