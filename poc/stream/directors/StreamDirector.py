import abc
from abc import ABC
from dataclasses import dataclass, field

from stream.Stream import Stream
from stream.commands.CommandInvoker import CommandInvoker


@dataclass
class StreamDirector(ABC):
    stream: Stream
    _in_stream_invoker: CommandInvoker = field(init=False, default_factory=CommandInvoker)
    _post_stream_invoker: CommandInvoker = field(init=False, default_factory=CommandInvoker)

    def __post_init__(self):
        self._init_in_stream_invoker()
        self._init_post_stream_invoker()

    def run(self):
        for _ in self.stream.get_next_frame_gen():
            self._in_stream_invoker.invoke()
        self._post_stream_invoker.invoke()

    @abc.abstractmethod
    def _init_in_stream_invoker(self):
        pass

    @abc.abstractmethod
    def _init_post_stream_invoker(self):
        pass
