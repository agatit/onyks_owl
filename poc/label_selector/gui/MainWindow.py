import tkinter as tk
from functools import partial
from pathlib import Path
from typing import Callable

import cv2
import numpy as np
from PIL import Image, ImageTk, ImageEnhance

from label_selector.gui.DrawCallback import DrawCallback
from label_selector.gui.LabelRectangle import LabelRectangle
from label_selector.gui.components.SideBar import SideBar
from label_selector.gui.components.TopBar import TopBar, TopBarLabels


class MainWindow(tk.Frame):
    START_POINT_THICKNESS: int = 4

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.original_image = None
        self.tk_image = None

        self.label_rectangles = []
        self.draw_callbacks: dict[str, DrawCallback] = {
            "label_rectangles": self._draw_label_rectangles,
        }

        top_bar = TopBar(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        self.top_bar = top_bar

        image_canvas = tk.Canvas(self, bg="grey")
        image_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.image_canvas = image_canvas

        side_bar = SideBar(self)
        side_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.side_bar = side_bar

        self.side_bar.gamma_value.trace("w", lambda *x: self.refresh_image())

        self.bind("<Configure>", lambda e: self.refresh_image())

    def load_image(self, img_path: Path, label_rectangles: list[LabelRectangle]) -> None:
        self.original_image = Image.open(img_path)
        self.label_rectangles = label_rectangles
        self.refresh_image()

    def set_info_with_timer(self, text: str, delay_ms: int) -> None:
        self.top_bar.set_label(TopBarLabels.INFO, text)
        self.after(delay_ms, lambda: self.top_bar.set_label(TopBarLabels.INFO, ''))

    def refresh_image(self) -> None:
        image_canvas = self.image_canvas
        image_canvas.update()

        if self.original_image is not None:
            canvas_size = image_canvas.winfo_width(), image_canvas.winfo_height()
            transformed_image = self.original_image.resize(canvas_size)
            transformed_image = self.adjust_brightness(transformed_image, self.side_bar.gamma_value.get() / 100)

            self.tk_image = ImageTk.PhotoImage(transformed_image)
            image_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            [callback(image_canvas) for callback in self.draw_callbacks.values()]

    # todo: przenieść na zewnątrz
    def _draw_label_rectangles(self, canvas: tk.Canvas) -> None:
        for label_rectangle in self.label_rectangles:
            color = label_rectangle.color
            bounding_box = label_rectangle.bounding_box

            x1y1 = self.resize_point_to_canvas(bounding_box.x1, bounding_box.y1)
            x2y2 = self.resize_point_to_canvas(bounding_box.x2, bounding_box.y2)

            self.draw_label_rectangle(canvas, x1y1, x2y2, label_rectangle.full_label, color)

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

    @staticmethod
    def draw_label_rectangle(image_canvas: tk.Canvas, x1y1: tuple[int, int], x2y2: tuple[int, int], text: str,
                             color: str = "red") -> None:
        image_canvas.create_rectangle(x1y1, x2y2, outline=color)

        label_x1y1 = (x1y1[0], x1y1[1] - 6)
        image_canvas.create_text(label_x1y1, fill=color, text=text)

    @staticmethod
    def adjust_brightness(image: Image, gamma: float = 1.0):
        return ImageEnhance.Brightness(image).enhance(gamma)
