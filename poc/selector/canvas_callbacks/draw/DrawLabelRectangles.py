from tkinter import Canvas

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.ImageCanvas import ImageCanvas


def draw_label_rectangles(app: Selector, model: SelectorModel, image_canvas: ImageCanvas, canvas: Canvas) -> None:
    current_data = model.get_selector_data(app.current_index_var.get())

    for label_rectangle in current_data.label_rectangles:
        color = label_rectangle.color
        bounding_box = label_rectangle.bounding_box

        x1y1 = image_canvas.resize_point_to_canvas(bounding_box.x1, bounding_box.y1)
        x2y2 = image_canvas.resize_point_to_canvas(bounding_box.x2, bounding_box.y2)

        _draw_label_rectangle(canvas, x1y1, x2y2, label_rectangle.full_label, color)


def _draw_label_rectangle(image_canvas: Canvas, x1y1: tuple[int, int], x2y2: tuple[int, int], text: str,
                          color: str = "red") -> None:
    image_canvas.create_rectangle(x1y1, x2y2, outline=color)

    label_x1y1 = (x1y1[0], x1y1[1] - 6)
    image_canvas.create_text(label_x1y1, fill=color, text=text)
