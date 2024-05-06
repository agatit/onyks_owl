# from functools import partial
#
# from selector.LabelSelector import LabelSelector
#
#
from functools import partial
from tkinter import Image

from PIL import ImageEnhance

from selector.Selector import Selector


def change_image_brightness(app: Selector, target: str, *trace_args):
    transformation_name = "brightness"

    scale_var = app.nametowidget(target).scale_var
    callback = partial(_adjust_brightness, brightness=scale_var.get())

    app.main_window.image_transformations[transformation_name] = callback
    app.notify_listener("reload_image")


def _adjust_brightness(image: Image, brightness: float):
    brightness = brightness / 100
    return ImageEnhance.Brightness(image).enhance(brightness)
