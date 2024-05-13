from dataclasses import dataclass
from typing import Iterable

from ocr.datasets.FullDatasetPart import FullDatasetPart


@dataclass
class FullDataset:
    parts: Iterable[FullDatasetPart]

