from PIL import Image

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.ImageCanvas import ImageCanvas


def resize(app: Selector, model: SelectorModel, image_canvas: ImageCanvas, image: Image) -> Image:
    image_canvas = image_canvas.canvas
    canvas_size = image_canvas.winfo_width(), image_canvas.winfo_height()

    return image.resize(canvas_size)
