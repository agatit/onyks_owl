import tkinter

from label_selector.commands.Command import Command


class ForceSaveCommand(Command):
    def execute(self, event: tkinter.Event = None) -> bool:
        checkpoint = self.app.save_manager.get_latest_checkpoint()
        self.app.save_checkpoint(checkpoint.name)

    def undo(self) -> None:
        pass