import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from selector.gui.DrawCallback import DrawCallback, TransformationCallback
from selector.gui.LabelRectangle import LabelRectangle


class MainWindow(tk.Frame):
    START_POINT_THICKNESS: int = 4

    def __init__(self, parent: tk.Tk | tk.Frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.original_image = None
        self.image_canvas = None
        self.tk_image = None

        self.label_rectangles = []

        self.image_transformations: dict[str, TransformationCallback] = {
            "resize": self.resize_image,
        }

        self.draw_callbacks: dict[str, DrawCallback] = {
            "label_rectangles": self._draw_label_rectangles,
        }

        self.bind("<Configure>", lambda e: self.refresh_image())

    # todo: bez ustawiania canvasa
    def set_image_canvas(self, canvas: tk.Canvas):
        self.image_canvas = canvas

    def load_image(self, img_path: Path, label_rectangles: list[LabelRectangle]) -> None:
        self.original_image = Image.open(img_path)
        self.label_rectangles = label_rectangles
        self.refresh_image()

    def refresh_image(self) -> None:
        if self.original_image and self.image_canvas:
            image_canvas = self.image_canvas
            image_canvas.update()

            transformed_image = self.original_image
            for callback in self.image_transformations.values():
                transformed_image = callback(transformed_image)

            self.tk_image = ImageTk.PhotoImage(transformed_image)
            image_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            [callback(image_canvas) for callback in self.draw_callbacks.values()]

    # todo: przenieść na zewnątrz
    def resize_image(self, image: Image) -> Image:
        image_canvas = self.image_canvas
        canvas_size = image_canvas.winfo_width(), image_canvas.winfo_height()

        return image.resize(canvas_size)

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
