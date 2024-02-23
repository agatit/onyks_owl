import tkinter as tk
from itertools import cycle
from pathlib import Path
from typing import Callable, Any

from PIL import Image

from label_selector.Mode import Mode
from label_selector.ProcessData import ProcessData
from label_selector.gui.MainWindow import MainWindow
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


class LabelSelector(tk.Tk):
    MAX_HISTORY_LENGTH = 50

    def __init__(self, images: list[Path], labels: dict[int, str]):
        super().__init__()
        self.labels = labels
        self.process_data = [ProcessData(image) for image in images]

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

    def reload_main_window(self):
        self.reload_image()
        self.reload_status()
        self.reload_image_name()
        self.reload_counter()
        self.reload_label()

    def reload_status(self):
        status = self.process_data[self.current_index].status
        self.main_window.set_status(status)

    def reload_label(self):
        full_label = f"{self.selected_label_id}_{self.selected_label_text}"
        self.main_window.set_class_label(full_label)

    def reload_image_name(self):
        name = self.process_data[self.current_index].image_path.name
        self.main_window.set_image_name(name)

    def reload_counter(self):
        self.main_window.set_counter(self.current_index, self.max_index)

    def reload_image(self):
        current_process_data = self.process_data[self.current_index]
        current_image = current_process_data.image_path
        label_rectangle = current_process_data.label_rectangles

        self.main_window.load_image(current_image, label_rectangle)

    def bind_canvas(self, key_string: str, callback: Callable[[tk.Event], None]) -> None:
        self.main_window.image_canvas.bind(key_string, callback)

    def get_current_mode(self) -> str:
        true_modes = [i for i in self.modes if self.modes[i].status]
        return true_modes[0]

    def register_to_mode(self, mode_name: str, target: Any, key: str, callback: Callable) -> None:
        self.modes[mode_name].register(target, key, callback)

    def add_mode(self, mode_name: str) -> None:
        self.modes[mode_name] = Mode()

    # self.default_mode_handler.bind(key_string, callback)

    def activate_mode(self, mode_name: str):
        for mode in self.modes.values():
            mode.deactivate()

        self.modes[mode_name].activate()

    def register_command_in_history(self, command_type: type, *args, **kwargs) -> Callable[[tk.Event], None]:

        def wrapper(event: tk.Event) -> None:
            command = command_type(*args, **kwargs)

            if command.execute(event):
                self.command_history.append(command)
                print(self.command_history)
                # print([id(i) for i in self.command_history])

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
            print(self.command_history)
            # print(self.modes)



    def export_dataset_parts(self) -> list[YoloDatasetPart]:
        filtered = filter(lambda x: x.status and len(x.label_rectangles) > 0, self.process_data)

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
