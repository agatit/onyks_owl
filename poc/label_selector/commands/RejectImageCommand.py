from dataclasses import dataclass

from label_selector.commands.Command import Command

@dataclass
class RejectImageCommand(Command):
    def execute(self, event=None) -> bool:
        current_index = self.app.current_index
        status = self.app.process_data[current_index].status

        if status:
            self.app.process_data[current_index].status = False
            self.app.reload_status()
            return True
        else:
            return False

    def undo(self) -> None:
        current_index = self.app.current_index
        self.app.process_data[current_index].status = True
        self.app.reload_status()


