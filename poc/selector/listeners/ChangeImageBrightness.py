from functools import partial
from tkinter import Image

from PIL import ImageEnhance

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


def change_image_brightness(app: Selector, model: SelectorModel, target: str, *trace_args):
    transformation_name = "brightness"

    brightness = app.var_register.get_var_value("brightness_var")
    callback = partial(_adjust_brightness, brightness=brightness)

    app.main_window.image_transformations[transformation_name] = callback
    app.notify_listener("reload_image")


def _adjust_brightness(image: Image, brightness: float):
    brightness = brightness / 100
    return ImageEnhance.Brightness(image).enhance(brightness)
