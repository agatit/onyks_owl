import tkinter

from selector.commands.Command import Command


class ForceSaveCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        checkpoint = self.app.save_manager.get_latest_checkpoint()

        if checkpoint is not None:
            self.app.save_checkpoint(checkpoint.name)

    def undo(self) -> None:
        pass