from typing import Any

Mapper = dict[str, Any]


def map_to(mapper: Mapper, out_class: type) -> Any:
    return out_class(**mapper)
