import tkinter
from abc import ABC
from dataclasses import dataclass

from label_selector.commands.Command import Command

@dataclass
class ListBoxCommand(Command, ABC):
    listbox: tkinter.Listbox
