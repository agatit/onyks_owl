import tkinter as tk
from typing import Callable

from label_selector.gui.MainWindow import MainWindow
from yolo.YoloDataset import YoloDataset


class ManualSelector(tk.Tk):
    def __init__(self, dataset: YoloDataset):
        super().__init__()
        self.dataset = dataset

        self.to_export = False
        self.current_index = 0
        self.max_index = len(dataset.yolo_dataset_parts)
        self.parts_status = [True] * self.max_index
        self.command_history = []

        self.keyboard_handler = tk.Frame(self)
        self.keyboard_handler.focus_set()
        self.keyboard_handler.pack()

        self.geometry('400x300')
        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)
        # self.main_window.bind("<KeyPress-a>", lambda e: print("ee"))
        # self.main_window.image_canvas.bind("<KeyPress-a>", lambda e: print("ee"))
        self.main_window.image_canvas.bind("<Button-1>", lambda e: print("cc"))

        # init state
        self.reload_main_window()

    def reload_main_window(self):
        self.reload_image()
        self.reload_status()
        self.reload_counter()

    def reload_counter(self):
        self.main_window.set_counter(self.current_index, self.max_index)

    def reload_status(self):
        index = self.current_index
        status = self.parts_status[index]
        self.main_window.set_image_name(status)

    def reload_image(self):
        index = self.current_index
        current_image = self.dataset.yolo_dataset_parts[index].original_image_path
        self.main_window.load_image(current_image)

    def bind_keyboard(self, key_string: str, callback: Callable[[tk.Event], None]) -> None:
        self.keyboard_handler.bind(key_string, callback)

    def bind_canvas(self, key_string: str, callback: Callable[[tk.Event], None]) -> None:
        self.main_window.image_canvas.bind(key_string, callback)

    def register_command(self, command) -> Callable[[tk.Event], None]:
        def wrapper(event: tk.Event) -> None:
            if command.execute(None):
                self.command_history.append(command)
                print(self.command_history)

        return wrapper

    def undo(self, event: tk.Event) -> None:
        if len(self.command_history) > 0:
            self.command_history.pop().undo()
            print(self.command_history)
