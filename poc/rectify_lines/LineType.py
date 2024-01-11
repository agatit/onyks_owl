from dataclasses import dataclass, field

from display.RegionOfInterest import RegionOfInterest


@dataclass
class LineType:
    type: str
    max_dots_number: int
    roi: RegionOfInterest
    lines: list = field(default_factory=list)

