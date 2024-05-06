from dataclasses import dataclass

from ocr.datasets.BboxN import BboxN


@dataclass
class Bbox:
    x1: int
    y1: int
    width: int
    height: int

    def normalize(self, original_width: int, original_height: int) -> BboxN:
        x1, y1, width, height = self.x1, self.y1, self.width, self.height

        normalized_x1 = x1 / original_width
        normalized_y1 = y1 / original_height
        normalized_width = width / original_width
        normalized_height = height / original_height

        return BboxN(normalized_x1, normalized_y1, normalized_width, normalized_height)