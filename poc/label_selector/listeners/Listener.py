from typing import Protocol

from label_selector.LabelSelector import LabelSelector


class Listener(Protocol):
    def __call__(self, app: LabelSelector, target: str, *trace_args):
        pass
