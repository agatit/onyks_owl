from dataclasses import dataclass


@dataclass
class Result:
    name: str
    res: dict
    weights: dict
    standard_deviations: dict
    config: dict

    def __post_init__(self):
        self._format_name()

    def _format_name(self):
        self.name = self.name.replace('.', '_')
