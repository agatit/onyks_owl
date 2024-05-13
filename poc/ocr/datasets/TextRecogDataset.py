from dataclasses import dataclass
from typing import Iterable

from ocr.datasets.TextRecogDatasetPart import TextRecogDatasetPart


@dataclass
class TextRecogDataset:
    parts: Iterable[TextRecogDatasetPart]

    def to_dict(self) -> dict:
        ...