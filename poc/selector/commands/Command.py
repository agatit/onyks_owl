import abc
import tkinter
from abc import ABC
from dataclasses import dataclass, field

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.MainWindow import MainWindow


@dataclass
class Command(ABC):
    app: Selector = field(repr=False)
    model: SelectorModel = field(repr=False)

    @abc.abstractmethod
    def execute(self, event: tkinter.Event = None) -> bool:
        pass

    @abc.abstractmethod
    def undo(self) -> None:
        pass
