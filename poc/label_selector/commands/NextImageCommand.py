from label_selector.commands.Command import Command


class NextImageCommand(Command):
    def execute(self, event=None) -> bool:
        index = self.app.current_index_var.get()
        max_index = self.app.max_index

        if index < max_index - 1:
            self.app.current_index_var.set(self.app.current_index_var.get() + 1)
            return True
        else:
            return False

    def undo(self) -> None:
        self.app.current_index_var.set(self.app.current_index_var.get() - 1)

