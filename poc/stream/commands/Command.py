import abc
from abc import ABC
from dataclasses import dataclass

from stream import Stream


@dataclass
class Command(ABC):
    stream: Stream

    @abc.abstractmethod
    def execute(self) -> None:
        pass
