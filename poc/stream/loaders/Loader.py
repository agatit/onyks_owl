import abc
from abc import ABC
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Loader(ABC):
    input_path: Path

    @abc.abstractmethod
    def get_image_gen(self):
        pass
