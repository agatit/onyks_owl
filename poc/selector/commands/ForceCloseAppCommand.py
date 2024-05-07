from tkinter.messagebox import askyesno

from selector.commands.Command import Command


class ForceCloseAppCommand(Command):
    MSG_TITLE = 'Confirmation'
    MESSAGE = 'Are you sure that you want to quit?'

    def execute(self, event=None) -> bool:
        current_index = self.app.current_index_var.get()
        next_index = current_index + 1

        if next_index != self.model.get_data_len():
            result = askyesno(title=self.MSG_TITLE,
                              message=self.MESSAGE)
            if result:
                self.app.destroy()

        return True

    def undo(self) -> bool:
        pass
