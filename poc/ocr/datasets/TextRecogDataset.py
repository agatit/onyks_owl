from dataclasses import dataclass

from ocr.datasets.TextRecogDatasetPart import TextRecogDatasetPart


@dataclass
class TextRecogDataset:
    parts: list[TextRecogDatasetPart]

    def to_dict(self) -> dict:
        ...