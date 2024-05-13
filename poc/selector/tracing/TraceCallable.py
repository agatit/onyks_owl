from typing import Protocol


class TraceCallable(Protocol):
    def __call__(self, var, index, mode) -> None: ...
