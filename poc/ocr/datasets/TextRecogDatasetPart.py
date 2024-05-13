from dataclasses import dataclass


@dataclass
class Instance:
    text: str


@dataclass
class TextRecogDatasetPart:
    instances: list[Instance]
    img_path: str
