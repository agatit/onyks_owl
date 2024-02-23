from tkinter import messagebox

from label_selector.commands.Command import Command


class CloseAppCommand(Command):
    def execute(self, event=None) -> bool:
        index = self.app.current_index
        max_index = self.app.max_index


        if index == max_index - 1:
            answer = messagebox.askyesno("Question", "Do you want to end?", )

            if answer:
                self.app.to_export = True
                self.app.destroy()

        return True

    def undo(self) -> bool:
        pass
