import abc
import pickle
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Checkpoint:
    name: str
    save_dir: Path
    period: int

    silent: bool = True
    full_path: Path = field(init=False)

    def __post_init__(self):
        self.reload_full_path()

    def change_name(self, name: str):
        self.name = name
        self.reload_full_path()

    def reload_full_path(self):
        self.full_path = self.save_dir / self.name

    def save(self, data: Any) -> None:
        self._dump_to_pickle(data)

    def load(self) -> Any:
        return self._load_from_pickle()

    def _dump_to_pickle(self, data: Any) -> None:
        with open(self.full_path, 'wb') as file:
            pickle.dump(data, file)

    def _load_from_pickle(self) -> Any:
        try:
            with open(self.full_path, 'rb') as file:
                data = pickle.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"No checkpoint file: {self.full_path}")
        except TypeError:
            raise FileNotFoundError(f"Any checkpoint file")

        return data


def init_checkpoint(name: str, save_dir: str, period: int, silent: bool, **kwargs):
    path = Path(save_dir)
    return Checkpoint(name, path, period, silent)
