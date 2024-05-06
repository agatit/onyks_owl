from tkinter import Canvas
from typing import Protocol

from PIL.Image import Image


class DrawCallback(Protocol):
    def __call__(self, canvas: Canvas) -> None:
        ...


class TransformationCallback(Protocol):
    def __call__(self, image: Image) -> Image:
        ...
