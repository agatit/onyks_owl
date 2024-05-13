from enum import Enum
from typing import Any, Protocol


class Mapper(Protocol):
    def __call__(self, *args, **kwargs) -> dict:
        ...

def map_to(mapper: Mapper, out_class: type) -> Any:
    return out_class(**mapper())

