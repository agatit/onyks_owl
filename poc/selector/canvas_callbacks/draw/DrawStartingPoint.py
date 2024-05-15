from tkinter import Canvas

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.ImageCanvas import ImageCanvas


def draw_starting_point(canvas: Canvas, x: int, y: int, thickness: int = 4) -> None:
    x1y1 = (x - thickness, y - thickness)
    x2y2 = (x + thickness, y + thickness)

    # return self.image_canvas.create_rectangle(x1y1, x2y2, fill="red")
    canvas.create_rectangle(x1y1, x2y2, fill="red")
