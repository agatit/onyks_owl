import tkinter
from tkinter import messagebox
from tkinter.messagebox import showinfo

from selector.commands.Command import Command


class CloseAppCommand(Command):
    EXIT_TITLE = "Confirmation"
    EXIT_MESSAGE = "Do you want to end?"
    INFO_TITLE = "Information"
    INFO_MESSAGE = "To end program you need to go to the last image"

    def execute(self, event=None) -> bool:
        index = self.app.current_index_var.get()
        max_index = self.model.get_data_len()

        # todo: zmienić na coś innego
        if isinstance(event.widget, tkinter.Listbox):
            return True

        if index == max_index - 1:
            answer = messagebox.askyesno(self.EXIT_TITLE, self.EXIT_MESSAGE, )

            if answer:
                self.model.to_export = True
                self.app.destroy()
        else:
            showinfo(self.INFO_TITLE, self.INFO_MESSAGE)

        return True

    def undo(self) -> bool:
        pass
