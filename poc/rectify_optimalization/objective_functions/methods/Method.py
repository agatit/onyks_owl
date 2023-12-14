from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union

import numpy as np

from display.RegionOfInterest import RegionOfInterest
from rectify_optimalization.objective_functions.methods.line_part_selectors.LinePartSelector import LinePartSelector
from rectify_optimalization.objective_functions.methods.line_types.LineType import LineType


@dataclass
class Method(ABC):
    id: str = field(init=False)
    name_type: str = field(init=False)
    lines: Union[list, np.ndarray]
    weight: float
    line_type: LineType
    line_part_selector: LinePartSelector
    roi: RegionOfInterest

    def __post_init__(self):
        self.lines = self.line_type.select(self.lines)

        self.id = self._generate_name(self, self.line_type, self.line_part_selector)
        self.name_type = str(self.id)

        self.id += f"_{self.weight}"

    @abstractmethod
    def _calc(self, rectified_lines) -> np.ndarray:
        pass

    def calculate(self, rectified_lines) -> np.ndarray:
        return self._calc(rectified_lines)

    def crop_points_from_roi(self, min_points: int = 3) -> None:
        roi = self.roi
        x = self.lines[:, :, 0]
        y = self.lines[:, :, 1]

        x_con = np.all((x >= roi.x1, x <= roi.x2), axis=0)
        y_con = np.all((y >= roi.y1, y <= roi.y2), axis=0)
        x_y_con = np.all((x_con, y_con), axis=0)
        counted_points_in_bounds = np.count_nonzero(x_y_con, axis=1)

        lines_with_min_points_con = counted_points_in_bounds >= min_points
        filterd_counted_points_in_bounds = counted_points_in_bounds[lines_with_min_points_con]
        most_common_number_points_in_lines = np.bincount(filterd_counted_points_in_bounds).argmax()

        valid_points_indexes = np.column_stack(np.where(x_y_con))

        filtered_lines = []
        for line_index, valid_points_number in enumerate(counted_points_in_bounds):
            if valid_points_number >= most_common_number_points_in_lines:
                current_line_con = valid_points_indexes[:, 0] == line_index
                points_indexes = valid_points_indexes[current_line_con][:most_common_number_points_in_lines, 1]

                filtered_line = self.lines[line_index, points_indexes]
                filtered_lines.append(filtered_line)
            else:
                continue

        self.lines = np.array(filtered_lines)

    @staticmethod
    def _generate_name(*classes):
        classes_name = (type(i).__name__ for i in classes)
        return "_".join(classes_name)
