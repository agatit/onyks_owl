from dataclasses import dataclass

from ocr.datasets.FullDatasetPart import FullDatasetPart


@dataclass
class FullDataset:

    parts: list[FullDatasetPart]


