from abc import ABC

from stream.YoloStream import YoloStream
from stream.commands.Command import Command


class YoloCommand(Command, ABC):
    stream: YoloStream
