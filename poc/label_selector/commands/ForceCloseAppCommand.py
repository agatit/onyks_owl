from tkinter.messagebox import askyesno

from label_selector.commands.Command import Command


class ForceCloseAppCommand(Command):
    MSG_TITLE = 'Confirmation'
    MESSAGE = 'Are you sure that you want to quit?'

    def execute(self, event=None) -> bool:

        # todo : zmiana na flagę w zapisie
        current_index = self.app.current_index
        next_index = current_index + 1

        if next_index != self.app.max_index:
            result = askyesno(title=self.MSG_TITLE,
                              message=self.MESSAGE)
            if result:
                self.app.destroy()

        return True

    def undo(self) -> bool:
        pass
