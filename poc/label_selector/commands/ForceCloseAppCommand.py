from tkinter.messagebox import askyesno

from label_selector.commands.Command import Command


class ForceCloseAppCommand(Command):
    MSG_TITLE = 'Confirmation'
    MESSAGE = 'Are you sure that you want to quit?'

    def execute(self, event=None) -> bool:
        result = askyesno(title=self.MSG_TITLE,
                          message=self.MESSAGE)
        if result:
            self.app.destroy()

        return True

    def undo(self) -> bool:
        pass
