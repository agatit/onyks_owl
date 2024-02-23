from label_selector.commands.Command import Command


class NextImageCommand(Command):
    def execute(self, event=None) -> bool:
        index = self.app.current_index
        max_index = self.app.max_index

        if index < max_index - 1:
            self.app.current_index += 1
            self.app.reload_main_window()
            return True
        else:
            return False

    def undo(self) -> None:
        self.app.current_index -= 1
        self.app.reload_main_window()
