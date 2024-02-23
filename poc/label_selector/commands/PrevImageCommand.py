from label_selector.commands.Command import Command


class PrevImageCommand(Command):
    def execute(self, event=None) -> bool:
        index = self.app.current_index

        if index > 0:
            self.app.current_index -= 1
            self.app.reload_main_window()
            return True
        else:
            return False

    def undo(self) -> None:
        self.app.current_index += 1
        self.app.reload_main_window()
