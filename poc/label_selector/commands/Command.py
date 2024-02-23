import abc
import tkinter
from abc import ABC
from dataclasses import dataclass, field

from label_selector.LabelSelector import LabelSelector
from label_selector.gui.MainWindow import MainWindow


@dataclass
class Command(ABC):
    app: LabelSelector = field(repr=False)
    main_window: MainWindow = field(repr=False)

    @abc.abstractmethod
    def execute(self, event: tkinter.Event = None) -> bool:
        pass

    @abc.abstractmethod
    def undo(self) -> None:
        pass
