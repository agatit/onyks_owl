import abc
import tkinter as tk
from abc import ABC
from typing import Callable, Any

from selector.Mode import Mode
from selector.tracing.TraceRegister import VarRegister


class Selector(tk.Tk, ABC):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.__class__.__name__)
        self.start_drawing_point = tuple()

        self.main_window = None
        self.current_label_text = None
        self.total_changed_index = 0

        self.var_register = VarRegister()
        self._command_history = []
        self._modes = {}
        self._listeners = {}

        self._init_main_window()
        self._init_variables()

        self._init_commands()
        self._init_listeners()
        self._init_canvas_callbacks()

        self.focus_force()

    @abc.abstractmethod
    def _init_main_window(self):
        pass

    @abc.abstractmethod
    def _init_commands(self):
        pass

    @abc.abstractmethod
    def _init_listeners(self):
        pass

    @abc.abstractmethod
    def _init_canvas_callbacks(self):
        pass

    # todo: komunikacja ze zmiennymi za pomocą VarRegister
    def _init_variables(self):
        self.current_index_var = tk.IntVar(self, 0)
        self.var_register.add_var("current_index_var", self.current_index_var)

        self.current_label_id_var = tk.IntVar(self, 0)
        self.var_register.add_var("current_label_id_var", self.current_label_id_var)

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
