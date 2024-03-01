import pickle
import tkinter as tk
from itertools import cycle
from pathlib import Path
from typing import Callable, Any

from PIL import Image

from label_selector.Mode import Mode
from label_selector.ProcessData import ProcessData
from label_selector.gui.LabelRectangle import LabelRectangle
from label_selector.gui.LoadingScreen import LoadingScreen
from label_selector.gui.MainWindow import MainWindow
from label_selector.Checkpoint import Checkpoint
from yolo.YoloDataset import YoloDataset
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


class LabelSelector(tk.Tk):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, images: list[Path], labels: dict[int, str], checkpoint_name=".checkpoint"):
        super().__init__()
        self.title(self.__class__.__name__)

        self.process_data = [ProcessData(image) for image in images]
        self.labels = labels
        self.checkpoint_name = checkpoint_name

        self.checkpoint_dir = Path.cwd()
        self.checkpoint_path = self.checkpoint_dir / self.checkpoint_name

        self.to_export = False
        self.start_point = tuple()

        self.current_index = 0
        self.max_index = len(self.process_data)
        self.selected_label_id = 0
        self.selected_label_text = labels[0]
        self.labels_id_cycle = cycle(labels.keys())
        self.labels_text_cycle = cycle(labels.values())

        self.command_history = []
        self.modes = {}

        self.geometry('800x600')
        self.main_window = MainWindow(self)
        self.main_window.pack(anchor="center", fill="both", expand=True)

        # init state
        self.reload_main_window()

    @classmethod
    def from_yolo_dataset(cls, dataset: YoloDataset, labels: dict[int, str]):
        images = [i.original_image_path for i in dataset.yolo_dataset_parts]
        checkpoint_name = '.' + dataset.dataset_name

        self = cls(images, labels, checkpoint_name)

        loading_screen = LoadingScreen(self)

        for process_data, dataset_part, in zip(self.process_data, dataset.yolo_dataset_parts):
            formats = dataset_part.yolo_formats

            label_rectangles = []
            for _format in formats:
                width, height = Image.open(dataset_part.original_image_path).size

                bounding_box = _format.to_bounding_box(width, height)

                label_rectangle = LabelRectangle(
                    label_id=_format.class_id,
                    label_text=labels[_format.class_id],
                    bounding_box=bounding_box
                )
                label_rectangles.append(label_rectangle)

            process_data.label_rectangles = label_rectangles

        self.reload_main_window()

        loading_screen.destroy()
        self.deiconify()

        return self

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
        full_label = f"{self.selected_label_id}_{self.selected_label_text}"
        self.main_window.set_class_label(full_label)

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

            yolo_formats = []
            for label_rectangle in process_data.label_rectangles:
                class_id = label_rectangle.label_id
                bounding_box = label_rectangle.bounding_box
                width, height = Image.open(image_path).size

                yolo_format = YoloFormat.from_bounding_box(class_id, width, height, bounding_box)
                yolo_formats.append(yolo_format)

            dataset_part = YoloDatasetPart(image_path, yolo_formats)
            dataset_parts.append(dataset_part)

        return dataset_parts

    def save_checkpoint(self) -> None:
        index = self.current_index
        checkpoint = Checkpoint(index, self.process_data)

        with open(self.checkpoint_path, 'wb') as file:
            pickle.dump(checkpoint, file)

    def load_checkpoint(self) -> None:
        try:
            with open(self.checkpoint_path, 'rb') as file:
                checkpoint = pickle.load(file)
        except FileNotFoundError:
            raise Exception(f"No checkpoint file: {self.checkpoint_name} found")

        self.current_index = checkpoint.current_index
        self.process_data = checkpoint.process_data

        self.reload_main_window()
