from ast import literal_eval
from typing import Any, Protocol, runtime_checkable


def literal_to_tuple(dictionary: dict, keys: list) -> dict:
    result = {}

    for key, value in dictionary.items():
        result[key] = value

        if key in keys:
            result[key] = literal_eval(value)

    return result

class LoaderFunction(Protocol):
    def __call__(self, **kwargs) -> Any:
        pass


Options = dict[str, LoaderFunction]


def init_options(options: Options, config: dict) -> list[Any]:
    results = []

    for option_name, loader_function in options.items():
        if not config[option_name]["active"]:
            continue

        result = loader_function(**config[option_name])
        results.append(result)

    return results
