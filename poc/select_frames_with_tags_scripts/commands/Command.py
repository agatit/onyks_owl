import abc
import tkinter
from abc import ABC
from dataclasses import dataclass

from select_frames_with_tags_scripts.gui.MainWindow import MainWindow


@dataclass
class Command(ABC):
    app: tkinter.Tk
    main_window: MainWindow

    @abc.abstractmethod
    def execute(self):
        pass
