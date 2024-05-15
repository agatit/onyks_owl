from typing import Protocol

from PIL.Image import Image


class TransformationCallback(Protocol):
    def __call__(self, image: Image) -> Image:
        ...
