from dataclasses import dataclass


@dataclass
class TextRecogDatasetPart:
    instances: list[str]
    img_path: str
