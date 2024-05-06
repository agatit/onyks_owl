from selector.commands.Command import Command


class PrevImageCommand(Command):
    def execute(self, event=None) -> bool:
        index = self.app.current_index_var.get()

        if index > 0:
            self.app.current_index_var.set(self.app.current_index_var.get() - 1)
            return True
        else:
            return False

    def undo(self) -> None:
        self.app.current_index_var.set(self.app.current_index_var.get() + 1)
