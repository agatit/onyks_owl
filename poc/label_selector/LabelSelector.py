import pickle
import tkinter as tk
from itertools import cycle
from os import access, R_OK
from pathlib import Path
from typing import Callable, Any

from PIL import Image

from label_selector.Checkpoint import Checkpoint
from label_selector.Mode import Mode
from label_selector.ProcessData import ProcessData
from label_selector.gui.MainWindow import MainWindow
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


class LabelSelector(tk.Tk):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, images: list[Path], labels: dict[int, str], checkpoint_name="checkpoint",
                 max_images: int = -1):
        super().__init__()
        self.title(self.__class__.__name__)

        if max_images < 0:
            images_to_load = len(images)
        else:
            images_to_load = max_images

        self.process_data = [ProcessData(image) for image in images[:images_to_load]]
        self.labels = labels
        self.checkpoint_name = checkpoint_name
        self.periodic_checkpoint_name = checkpoint_name + "_tmp"

        self.checkpoint_dir = Path.cwd()
        self.checkpoint_path = self.checkpoint_dir / self.checkpoint_name
        self.periodic_checkpoint_path = self.checkpoint_dir / self.periodic_checkpoint_name

        self.to_export = False
        self.start_point = tuple()

        self._current_index = 0
        self.current_label_id = 0
        self.current_label_text = labels[self.current_label_id]
        self.max_index = len(self.process_data)

        self.total_changed_index = 0

        self.command_history = []
        self.modes = {}

        self.geometry('800x600')
        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)

        # init state
        self.reload_main_window()

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, value):
        self.total_changed_index += 1
        self._current_index = value

    def reload_main_window(self):
        self.reload_image()
        self.reload_image_name()
        self.reload_counter()
        self.reload_label()

    def reload_image(self):
        current_process_data = self.process_data[self.current_index]
        current_image = current_process_data.image_path
        label_rectangle = current_process_data.label_rectangles

        self.main_window.load_image(current_image, label_rectangle)

    def reload_image_name(self):
        name = self.process_data[self.current_index].image_path.name
        self.main_window.set_image_name(name)

    def reload_counter(self):
        self.main_window.set_counter(self.current_index, self.max_index)

    def reload_label(self):
        self.main_window.set_class_label(self.current_label_text)

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

    def save_checkpoint(self, path: Path) -> None:
        index = self.current_index
        checkpoint = Checkpoint(index, self.process_data)
        self._dump_checkpoint(path, checkpoint)

    @staticmethod
    def _dump_checkpoint(path: Path, data: Any):
        with open(path, 'wb') as file:
            pickle.dump(data, file)

    def load_checkpoint(self) -> None:
        last_checkpoint = self._select_latest_checkpoint()

        if last_checkpoint:
            self._load_from_pickle(last_checkpoint)

    def _select_latest_checkpoint(self) -> Any:
        checkpoints = [
            self.checkpoint_path,
            self.periodic_checkpoint_path
        ]

        checkpoints = [i for i in checkpoints if i.exists() and i.stat().st_size > 0]

        if len(checkpoints) > 0:
            checkpoints.sort(key=lambda p: p.stat().st_mtime)
            return checkpoints.pop()
        else:
            return None

    def _load_from_pickle(self, path: Path) -> Any:
        try:
            with open(path, 'rb') as file:
                data = pickle.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"No checkpoint file: {self.checkpoint_name}")
        except TypeError:
            raise FileNotFoundError(f"Any checkpoint file")

        return data
