from typing import Protocol

from selector.Selector import Selector


class Listener(Protocol):
    def __call__(self, app: Selector, target: str, *trace_args):
        pass
