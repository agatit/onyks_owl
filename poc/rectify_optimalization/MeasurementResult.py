from dataclasses import dataclass


@dataclass
class MeasurementResult:
    name: str
    roi: tuple[int, int, int, int]
    res: dict
    weights: dict
    standard_deviations: dict
    config: dict

    def __post_init__(self):
        self._format_name()

    def _format_name(self):
        self.name = self.name.replace('.', '_')
