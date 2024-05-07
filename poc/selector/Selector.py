import abc
import tkinter as tk
from abc import ABC
from pathlib import Path
from typing import Callable, Any, Protocol

from PIL import Image

from selector.Mode import Mode
from selector.ProcessData import ProcessData
from selector.SelectorModel import SelectorModel

from selector.saving.SaveManager import SaveManager
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


class Selector(tk.Tk, ABC):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.__class__.__name__)
        self.start_drawing_point = tuple()

        self.current_index_var = tk.IntVar(self, 0, "current_index_var")
        self.current_label_id_var = tk.IntVar(self, 0, "current_label_id_var")

        # self.current_label_text = labels[self.current_label_id_var.get()]
        self.current_label_text = None
        # self.max_index = len(self.process_data)

        self.total_changed_index = 0

        self._command_history = []
        self._modes = {}
        self._listeners = {}

        self.main_window = None
        self._init_main_window()
        self._init_commands()
        self._init_listeners()

    @abc.abstractmethod
    def _init_main_window(self):
        pass

    @abc.abstractmethod
    def _init_commands(self):
        pass

    @abc.abstractmethod
    def _init_listeners(self):
        pass

    # def get_current_process_data(self) -> ProcessData:
    #     return self.process_data[self.current_index_var.get()]

    def get_current_mode(self) -> str:
        true_modes = [i for i in self._modes if self._modes[i].status]
        return true_modes[0]

    def register_to_mode(self, mode_name: str, target: Any, key: str, callback: Callable) -> None:
        self._modes[mode_name].register(target, key, callback)

    def add_mode(self, mode_name: str) -> None:
        self._modes[mode_name] = Mode()

    def activate_mode(self, mode_name: str):
        for mode in self._modes.values():
            mode.deactivate()

        self._modes[mode_name].activate()

    def add_listener(self, listener_name: str, callback: Callable) -> None:
        self._listeners[listener_name] = callback

    def notify_listener(self, listener_name: str):
        if listener_name in self._listeners:
            self._listeners[listener_name]()

    def register_command_in_history(self, command_type: type, *args, **kwargs) -> Callable[[tk.Event], None]:

        def wrapper(event: tk.Event) -> None:
            command = command_type(*args, **kwargs)

            if command.execute(event):
                self._command_history.append(command)

            if len(self._command_history) > self.MAX_HISTORY_LENGTH:
                self._command_history.pop(0)

        return wrapper

    @staticmethod
    def register_command_without_history(command_type: type, *args, **kwargs) -> Callable[[tk.Event], None]:
        def wrapper(event: tk.Event) -> None:
            command = command_type(*args, **kwargs)
            command.execute(event)

        return wrapper

    def undo(self) -> None:
        # print(self._command_history)
        if len(self._command_history) > 0:
            self._command_history.pop().undo()





    # def save_checkpoint(self, checkpoint_name: str):
    #     checkpoint_data = (self.to_export, self.current_index_var.get(), self.process_data)
    #     checkpoint = self.save_manager.get_checkpoint(checkpoint_name)
    #     checkpoint.save(checkpoint_data)

    # def load_checkpoint(self) -> None:
    #     checkpoint = self.save_manager.get_latest_checkpoint()
    #
    #     if checkpoint is not None:
    #         data = checkpoint.load()
    #
    #         self.to_export = data[0]
    #         self.process_data = data[2]
    #
    #         self.current_index_var.set(data[1])
    #         # self.reload_main_window()
    #         self.notify_listener("reload_main_window")
