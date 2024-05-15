import tkinter as tk
from pathlib import Path

from PIL import ImageTk, Image

from selector.canvas_callbacks.draw.DrawCallback import DrawCallback
from selector.canvas_callbacks.transform.TransformationCallback import TransformationCallback


class ImageCanvas(tk.Frame):
    def __init__(self, parent: tk.Frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg="grey")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.original_image = None
        self.tk_image = None

        # self.current_image_path = tk.StringVar(self)

        self.image_transformations: dict[str, TransformationCallback] = {}
        self.draw_callbacks: dict[str, DrawCallback] = {}

        self.bind("<Configure>", lambda e: self.refresh_image())

    def load_image(self, img_path: Path) -> None:
        self.original_image = Image.open(img_path)
        # self.label_rectangles = label_rectangles

        self.refresh_image()

    def refresh_image(self) -> None:
        if self.original_image and self.canvas:
            image_canvas = self.canvas
            image_canvas.update()

            transformed_image = self.original_image
            for callback in self.image_transformations.values():
                transformed_image = callback(transformed_image)

            self.tk_image = ImageTk.PhotoImage(transformed_image)
            image_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            [callback(image_canvas) for callback in self.draw_callbacks.values()]

    def resize_point_to_original(self, x: int, y: int) -> tuple[int, int]:
        image_canvas = self.canvas

        current_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        original_size = self.original_image.size

        new_x = int(x * original_size[0] / current_size[0])
        new_y = int(y * original_size[1] / current_size[1])
        return new_x, new_y

    def resize_point_to_canvas(self, x: int, y: int) -> tuple[int, int]:
        image_canvas = self.canvas
        current_size = image_canvas.winfo_width(), image_canvas.winfo_height()
        original_size = self.original_image.size

        new_x = int(x * current_size[0] / original_size[0])
        new_y = int(y * current_size[1] / original_size[1])
        return new_x, new_y
