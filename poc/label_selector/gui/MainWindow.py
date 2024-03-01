from dataclasses import dataclass
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from label_selector.gui.LabelRectangle import LabelRectangle


class MainWindow(tk.Frame):
    START_POINT_THICKNESS: int = 4

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.original_image = None
        self.tk_image = None

        self.label_rectangles = []

        labels_container = tk.Frame(self)
        self.labels_container = labels_container

        info_label = tk.Label(labels_container, text="", width=10, anchor=tk.W)
        info_label.pack(side=tk.LEFT, expand=False)
        self.info_label = info_label

        class_label = tk.Label(labels_container, text="class", width=30)
        class_label.pack(side=tk.LEFT, expand=True)
        self.class_label = class_label

        image_name = tk.Label(labels_container, text="Image", width=40)
        image_name.pack(side=tk.LEFT, expand=True)
        self.image_name = image_name

        counter_label = tk.Label(labels_container, text="counter", width=10, anchor=tk.E)
        counter_label.pack(side=tk.LEFT, expand=False)
        self.counter_label = counter_label

        labels_container.pack(side=tk.TOP, fill=tk.X)

        image_canvas = tk.Canvas(self, bg="blue")
        image_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.image_canvas = image_canvas

        self.bind("<Configure>", lambda e: self.refresh_image())

    def load_image(self, img_path: Path, label_rectangles: list[LabelRectangle]) -> None:
        self.original_image = Image.open(img_path)
        self.label_rectangles = label_rectangles
        self.refresh_image()

    def set_info_with_timer(self, text: str, delay_ms: int) -> None:
        self.info_label.config(text=text)
        self.after(delay_ms, lambda: self.info_label.config(text=''))

    def set_class_label(self, text: str) -> None:
        self.class_label.config(text=text)

    def set_image_name(self, text: str) -> None:
        self.image_name.config(text=text)

    def set_counter(self, current: int, max_number: int) -> None:
        text = f"{current + 1}/{max_number}"
        self.counter_label.config(text=text)

    def refresh_image(self) -> None:
        image_canvas = self.image_canvas

        image_canvas.update()
        canvas_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        resized_image = self.original_image.resize(canvas_size)

        self.tk_image = ImageTk.PhotoImage(resized_image)
        image_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self._draw_on_canvas()

    def _draw_on_canvas(self):
        for label_rectangle in self.label_rectangles:
            bounding_box = label_rectangle.bounding_box
            x1y1 = self.resize_point_to_canvas(bounding_box.x1, bounding_box.y1)
            x2y2 = self.resize_point_to_canvas(bounding_box.x2, bounding_box.y2)

            self.draw_label_rectangle(x1y1, x2y2, label_rectangle.full_label)

    def resize_point_to_original(self, x: int, y: int) -> tuple[int, int]:
        image_canvas = self.image_canvas

        current_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        original_size = self.original_image.size

        new_x = int(x * original_size[0] / current_size[0])
        new_y = int(y * original_size[1] / current_size[1])
        return new_x, new_y

    def resize_point_to_canvas(self, x: int, y: int) -> tuple[int, int]:
        image_canvas = self.image_canvas
        current_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        original_size = self.original_image.size

        new_x = int(x * current_size[0] / original_size[0])
        new_y = int(y * current_size[1] / original_size[1])
        return new_x, new_y

    def draw_start_point(self, x: int, y: int) -> int:
        thickness = self.START_POINT_THICKNESS

        x1y1 = (x - thickness, y - thickness)
        x2y2 = (x + thickness, y + thickness)

        return self.image_canvas.create_rectangle(x1y1, x2y2, fill="red")

    def draw_label_rectangle(self, x1y1: tuple[int, int], x2y2: tuple[int, int], text: str) -> None:
        self.image_canvas.create_rectangle(x1y1, x2y2, outline='red')

        label_x1y1 = (x1y1[0] + 6, x1y1[1] - 6)
        self.image_canvas.create_text(label_x1y1, fill="red", text=text)
