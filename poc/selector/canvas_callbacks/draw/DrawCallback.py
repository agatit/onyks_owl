from tkinter import Canvas
from typing import Protocol


class DrawCallback(Protocol):
    def __call__(self, canvas: Canvas, **kwargs) -> None:
        ...
