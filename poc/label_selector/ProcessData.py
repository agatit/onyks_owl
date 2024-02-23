from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from label_selector.gui.LabelRectangle import LabelRectangle


@dataclass
class ProcessData:
    image_path: Path
    label_rectangles: list[LabelRectangle] = field(default_factory=list)

    status: bool = True
    start_point_ref: int = field(init=False)

