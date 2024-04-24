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

        self._current_index = 0
        self._current_label_id = 0
        self.current_label_text = labels[self.current_label_id]
        self.max_index = len(self.process_data)

        self.total_changed_index = 0

        self.command_history = []
        self.modes = {}

        self.geometry('800x600')
        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)
        # self.init_side_bar()

        # self. tk.StringVar(value=dir(tk))
        _list = list(self.labels.values())
        self.classes_listbox_var = tk.StringVar(value=_list)
        self.main_window.side_bar.classes_listbox.listbox.config(listvariable=self.classes_listbox_var)

        self.results_listbox_var = tk.StringVar(value=_list)
        self.main_window.side_bar.results_listbox.listbox.config(listvariable=self.results_listbox_var)

        # init state
        self.reload_main_window()

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, value) -> None:
        self.total_changed_index += 1
        self._current_index = value

    @property
    def current_label_id(self) -> int:
        return self._current_label_id

    @current_label_id.setter
    def current_label_id(self, value: int) -> None:
        self._current_label_id = value
        self.current_label_text = self.labels[self._current_label_id]

    def get_current_process_data(self) -> ProcessData:
        return self.process_data[self.current_index]

    def reload_main_window(self):
        self.reload_image()
        self.reload_image_name()
        self.reload_counter()
        self.reload_label()
        self.reload_results_listbox()

    def reload_image(self):
        current_process_data = self.process_data[self.current_index]
        current_image = current_process_data.image_path
        label_rectangle = current_process_data.label_rectangles

        self.main_window.load_image(current_image, label_rectangle)

    def reload_image_name(self):
        name = self.process_data[self.current_index].image_path.name
        self.main_window.top_bar.set_label(TopBarLabels.IMAGE, name)

    def reload_counter(self):
        self.main_window.top_bar.set_counter(self.current_index, self.max_index)

    def reload_label(self):
        self.main_window.top_bar.set_label(TopBarLabels.ClASS, self.current_label_text)

    def reload_results_listbox(self):
        _list = [f"{label_rectangle.label_text}({i})" for i, label_rectangle
                 in enumerate(self.process_data[self._current_index].label_rectangles)]
        self.results_listbox_var.set(_list)

    def bind_canvas(self, key_string: str, callback: Callable[[tk.Event], None]) -> None:
        self.main_window.image_canvas.bind(key_string, callback)

    def get_current_mode(self) -> str:
        true_modes = [i for i in self.modes if self.modes[i].status]
        return true_modes[0]

    def register_to_mode(self, mode_name: str, target: Any, key: str, callback: Callable) -> None:
        self.modes[mode_name].register(target, key, callback)

    def add_mode(self, mode_name: str) -> None:
        self.modes[mode_name] = Mode()

    def activate_mode(self, mode_name: str):
        for mode in self.modes.values():
            mode.deactivate()

        self.modes[mode_name].activate()

    def register_command_in_history(self, command_type: type, *args, **kwargs) -> Callable[[tk.Event], None]:

        def wrapper(event: tk.Event) -> None:
            command = command_type(*args, **kwargs)

            if command.execute(event):
                self.command_history.append(command)

            if len(self.command_history) > self.MAX_HISTORY_LENGTH:
                self.command_history.pop(0)

        return wrapper

    @staticmethod
    def register_command_without_history(command_type: type, *args, **kwargs) -> Callable[[tk.Event], None]:
        def wrapper(event: tk.Event) -> None:
            command = command_type(*args, **kwargs)
            command.execute(event)

        return wrapper

    def undo(self) -> None:
        if len(self.command_history) > 0:
            self.command_history.pop().undo()

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
        checkpoint_data = (self.to_export, self.current_index, self.process_data)
        checkpoint = self.save_manager.get_checkpoint(checkpoint_name)
        checkpoint.save(checkpoint_data)

    def load_checkpoint(self) -> None:
        checkpoint = self.save_manager.get_latest_checkpoint()

        if checkpoint is not None:
            data = checkpoint.load()

            self.to_export = data[0]
            self.current_index = data[1]
            self.process_data = data[2]

            self.reload_main_window()
