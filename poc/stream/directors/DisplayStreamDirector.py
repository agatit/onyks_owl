from dataclasses import dataclass

from stream.commands.display.DestroyWindowsCommand import DestroyWindowsCommand
from stream.commands.display.DisplayStreamCommand import DisplayStreamCommand
from stream.commands.display.InterruptStreamCommand import InterruptStreamCommand
from stream.commands.transformation.RectifyCommand import RectifyCommand
from stream.commands.transformation.ScaleImageCommand import ScaleImageCommand
from stream.directors.StreamDirector import StreamDirector


@dataclass
class DisplayStreamDirector(StreamDirector):
    scale: int = 60

    def _init_in_stream_invoker(self):
        stream = self.stream
        invoker = self._in_stream_invoker

        invoker.add_command(RectifyCommand(stream))
        invoker.add_command(ScaleImageCommand(stream, self.scale))
        invoker.add_command(DisplayStreamCommand(stream))
        invoker.add_command(InterruptStreamCommand(stream))

    def _init_post_stream_invoker(self):
        stream = self.stream
        invoker = self._post_stream_invoker

        invoker.add_command(DestroyWindowsCommand(stream))
