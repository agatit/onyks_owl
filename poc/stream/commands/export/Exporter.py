import abc
from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from stream.commands.Command import Command


@dataclass
class Exporter(Command, ABC):
    output_path: Path

