from ast import literal_eval
from dataclasses import dataclass
from typing import Any


class FromYaml:
    def __init__(self, **attr):
        for name, value in attr.items():
            setattr(self, name, value)


def tuple_to_literal(dictionary: dict, keys: list) -> dict:
    result = {}

    for key, value in dictionary.items():
        result[key] = value

        if key in keys:
            result[key] = literal_eval(value)

    return result

