from dataclasses import dataclass, field
from typing import ClassVar

from yolo.YoloFormat import BoundingBox


@dataclass
class LabelRectangle:
    selected_color: ClassVar[str] = "green"
    unselected_color: ClassVar[str] = "red"

    label_id: int
    label_text: str
    bounding_box: BoundingBox

    full_label: str = field(init=False, repr=False)
    color: str = field(init=False, repr=False, default="red")
    _selected: bool = field(init=False, repr=False, default=False)

    def __post_init__(self):
        self.full_label = f"{self.label_id}:{self.label_text}"

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

        if self._selected:
            self.color = self.selected_color
        else:
            self.color = self.unselected_color
