from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Mode:
    status: bool = False
    __events: dict[Any, list[tuple[str, Callable]]] = field(default_factory=dict)

    def register(self, target: Any, event_str: str, callback: Callable) -> None:
        if target not in self.__events.keys():
            self.__events[target] = []

        self.__events[target].append((event_str, callback))

    def activate(self) -> None:
        if not self.status:
            for target, _list in self.__events.items():
                for key, callback in _list:
                    target.bind(key, callback)
            self.status = True

    def deactivate(self) -> None:
        if self.status:
            for target, _list, in self.__events.items():
                for key, _ in _list:
                    target.unbind(key)
            self.status = False
