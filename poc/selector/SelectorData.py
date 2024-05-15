from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from selector.gui.LabelRectangle import LabelRectangle


@dataclass(kw_only=True)
class SelectorData:
    image_path: Path
    label_rectangles: list[LabelRectangle] = field(default_factory=list)
