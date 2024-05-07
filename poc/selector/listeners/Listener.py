from typing import Protocol, Any

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel


class Listener(Protocol):
    def __call__(self, app: Selector, model: SelectorModel, target: str, *trace_args):
        pass
