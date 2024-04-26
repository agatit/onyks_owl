import tkinter as tk
from abc import ABC
from pathlib import Path
from typing import Callable, Any

from PIL import Image

from label_selector.Mode import Mode
from label_selector.ProcessData import ProcessData
from label_selector.gui.MainWindow import MainWindow
from label_selector.gui.components.TopBar import TopBarLabels

from label_selector.saving.SaveManager import SaveManager
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


class LabelSelector(tk.Tk):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, images: list[Path], labels: dict[int, str], save_manager: SaveManager,
                 max_images: int = -1, dataset_name: str = "dataset"):
        super().__init__()
        self.title(self.__class__.__name__)
        self.dataset_name = dataset_name

        if max_images < 0:
            images_to_load = len(images)
        else:
            images_to_load = max_images

        self.process_data = [ProcessData(image) for image in images[:images_to_load]]
        self.labels = labels
        self.save_manager = save_manager
        self.to_export = False

        self.start_point = tuple()

        self.current_index_var = tk.IntVar(self, 0, "current_index_var")
        self.current_label_id_var = tk.IntVar(self, 0, "current_label_id_var")

        self.current_label_text = labels[self.current_label_id_var.get()]
        self.max_index = len(self.process_data)

        self.total_changed_index = 0

        self._command_history = []
        self._modes = {}
        self._listeners = {}

        self.geometry('800x600')
        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)
        # self.init_side_bar()

        # self. tk.StringVar(value=dir(tk))
        _list = list(self.labels.values())
        self.classes_listbox_var = tk.StringVar(self, _list, "classes_listbox_var")
        self.main_window.side_bar.classes_listbox.listbox.config(listvariable=self.classes_listbox_var)

        self.results_listbox_var = tk.StringVar(self, _list, "results_listbox_var")
        self.main_window.side_bar.results_listbox.listbox.config(listvariable=self.results_listbox_var)

    def get_current_process_data(self) -> ProcessData:
        return self.process_data[self.current_index_var.get()]

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
        if len(self._command_history) > 0:
            self._command_history.pop().undo()

    def export_dataset_parts(self) -> list[YoloDatasetPart]:
        filtered = filter(lambda x: len(x.label_rectangles) > 0, self.process_data)

        dataset_parts = []
        for process_data in filtered:
            image_path = process_data.image_path
            yolo_formats = self._process_data_to_yolo_formats(process_data)

            dataset_part = YoloDatasetPart(image_path, yolo_formats)
            dataset_parts.append(dataset_part)

        return dataset_parts

    @staticmethod
    def _process_data_to_yolo_formats(process_data):
        image_path = process_data.image_path

        yolo_formats = []
        for label_rectangle in process_data.label_rectangles:
            class_id = label_rectangle.label_id
            bounding_box = label_rectangle.bounding_box
            width, height = Image.open(image_path).size

            yolo_format = YoloFormat.from_bounding_box(class_id, width, height, bounding_box)
            yolo_formats.append(yolo_format)

        return yolo_formats

    def save_checkpoint(self, checkpoint_name: str):
        checkpoint_data = (self.to_export, self.current_index_var.get(), self.process_data)
        checkpoint = self.save_manager.get_checkpoint(checkpoint_name)
        checkpoint.save(checkpoint_data)

    def load_checkpoint(self) -> None:
        checkpoint = self.save_manager.get_latest_checkpoint()

        if checkpoint is not None:
            data = checkpoint.load()

            self.to_export = data[0]
            self.process_data = data[2]

            self.current_index_var.set(data[1])

            # self.reload_main_window()
            self.notify_listener("reload_main_window")

