import tkinter as tk

from select_frames_with_tags_scripts.commands.Command import Command
from select_frames_with_tags_scripts.commands.CommandHistory import CommandHistory
from select_frames_with_tags_scripts.gui.MainWindow import MainWindow


class App(tk.Tk):
    def __init__(self, input_dir, output_dir):
        super().__init__()

        self.command_history = CommandHistory()

        self.geometry('400x300')

        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)

    def record_command(self, command: Command) -> Command:
        self.command_history.push(command)
        return command

    def get_keybinding(self):
        pass
