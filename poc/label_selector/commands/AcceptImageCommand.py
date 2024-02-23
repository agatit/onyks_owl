from dataclasses import dataclass, field

from label_selector.commands.Command import Command


@dataclass
class AcceptImageCommand(Command):
    def execute(self, event=None) -> bool:
        current_index = self.app.current_index
        status = self.app.process_data[current_index].status

        if not status:
            self.app.process_data[current_index].status = True
            self.app.reload_status()
            return True
        else:
            return False

    def undo(self) -> None:
        current_index = self.app.current_index
        self.app.process_data[current_index].status = False
        self.app.reload_status()
