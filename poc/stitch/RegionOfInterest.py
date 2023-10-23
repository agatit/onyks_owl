import numpy as np


class RegionOfInterest:
    def __init__(self, source_region_size, x1, y1, x2, y2):
        self.source_region_size = source_region_size
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.p1 = (x1, y1)
        self.p2 = (x2, y2)

        self.width = np.abs(x1 - x2)
        self.height = np.abs(y1 - y2)

    @classmethod
    def from_margin_percent(cls, source_region_size, top, right, bottom, left):
        width, height = source_region_size

        params = {
            "x1": cls.__percent_of_a_number(left, width),
            "y1": cls.__percent_of_a_number(top, height),
            "x2": width - cls.__percent_of_a_number(right, width),
            "y2": height - cls.__percent_of_a_number(bottom, height),
        }

        return cls(source_region_size, *params.values())

    @classmethod
    def from_margin_px(cls, source_region_size, top, right, bottom, left):
        width, height = source_region_size

        params = {
            "x1": left,
            "y1": top,
            "x2": width - right,
            "y2": height - bottom,
        }

        return cls(source_region_size, *params.values())

    def crop_numpy_array(self, array):
        return array[self.y1:self.y2, self.x1:self.x2]

    @staticmethod
    def __percent_of_a_number(percent, number):
        return int((percent / 100) * number)


