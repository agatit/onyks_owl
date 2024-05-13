import abc
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Iterable

from selector.SelectorData import SelectorData
from selector.saving.SaveManager import SaveManager


@dataclass(kw_only=True)
class SelectorModel(ABC):
    save_manager: SaveManager
    labels: dict[int, str]

    max_images: int = -1
    to_export: bool = False

    _selector_data: list[SelectorData] = field(init=False, default_factory=list)

    def __post_init__(self):
        self._init_selector_data()

    @abc.abstractmethod
    def _init_selector_data(self) -> None:
        ...

    @abc.abstractmethod
    def save_checkpoint(self, checkpoint_name: str, current_index: int):
        ...

    def get_selector_data(self, index: int) -> SelectorData:
        return self._selector_data[index]

    def get_all_selector_data(self) -> Iterable[SelectorData]:
        return self._selector_data

    def get_selector_data_len(self) -> int:
        return len(self._selector_data)
