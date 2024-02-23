from label_selector.commands.Command import Command


class ForceCloseAppCommand(Command):
    def execute(self, event=None) -> bool:
        self.app.destroy()
        return True

    def undo(self) -> bool:
        pass