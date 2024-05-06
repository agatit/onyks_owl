from dataclasses import dataclass, field

from ocr.datasets.Bbox import Bbox
from ocr.datasets.BboxN import BboxN
from ocr.datasets.Polygon import Polygon


@dataclass
class FullDatasetPart:
    src_file_name: str
    src_file_width: int
    src_file_height: int

    bbox: Bbox
    reg_text: str
    label_id: int

