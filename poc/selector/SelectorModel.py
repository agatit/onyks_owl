import abc
from abc import ABC
from dataclasses import dataclass
from typing import Any, Iterable

from selector.saving.SaveManager import SaveManager


@dataclass
class SelectorModel(ABC):
    save_manager: SaveManager
    labels: dict[int, str]

    @abc.abstractmethod
    def get_data(self, index: int) -> Any:
        ...

    @abc.abstractmethod
    def get_all_data(self) -> Any:
        ...

    @abc.abstractmethod
    def get_data_len(self) -> int:
        ...

    @abc.abstractmethod
    def save_checkpoint(self, checkpoint_name: str, current_index: int):
        ...
