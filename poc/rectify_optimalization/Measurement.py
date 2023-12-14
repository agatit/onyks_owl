import json
from dataclasses import dataclass, field
from itertools import product
from typing import Union, Iterator

import cv2
import numpy as np

from display.RegionOfInterest import RegionOfInterest
from io_utils.yaml import literal_to_tuple
from rectify_optimalization.objective_functions.methods.DistanceMethod import DistanceMethod
from rectify_optimalization.objective_functions.methods.Method import Method
from rectify_optimalization.objective_functions.methods.StdMethod import StdMethod
from rectify_optimalization.objective_functions.methods.line_part_selectors.XPoints import XPoints
from rectify_optimalization.objective_functions.methods.line_part_selectors.YPoints import YPoints
from rectify_optimalization.objective_functions.methods.line_types.Horizontal import Horizontal
from rectify_optimalization.objective_functions.methods.line_types.Vertical import Vertical


@dataclass
class Measurement:
    name: str
    lines_file_path: str
    image_path: str
    methods: Union[list[Method], dict]

    # todo: zmiana na loadera
    line_part_selector_types = {
        "XPoints": XPoints,
        "YPoints": YPoints,
    }
    line_types = {
        "Horizontal": Horizontal,
        "Vertical": Vertical
    }
    method_types = {
        "StdMethod": StdMethod,
        "DistanceMethod": DistanceMethod
    }

    def load_image(self) -> np.ndarray:
        return cv2.imread(self.image_path)

    def init_methods(self, consts) -> None:
        W, H = consts["W"], consts["H"]

        with open(self.lines_file_path, "r") as file:
            lines = json.load(file)

        # horizontal_lines = np.array(lines[0]["lines"], dtype=np.float64)
        # vertical_lines = np.array(lines[1]["lines"], dtype=np.float64)

        methods = []
        for init_method in self.methods:
            method_type = self.method_types[init_method["method"]]
            line_type = self.line_types[init_method["line_type"]]
            line_part_selector = self.line_part_selector_types[init_method["line_part"]]

            tuple_keys = ["weights_range", "roi"]
            init_method = literal_to_tuple(init_method, tuple_keys)

            for weigth in np.arange(*init_method["weights_range"]):
                lines_copy = lines.copy()

                _line_type = line_type()
                _line_part_selector = line_part_selector()
                roi = RegionOfInterest((W, H), *init_method["roi"])

                new_method = method_type(lines_copy, weigth, _line_type, _line_part_selector, roi)

                new_method.crop_points_from_roi()
                methods.append(new_method)

        self.methods = methods

    def get_methods_product(self) -> Iterator[Method]:
        methods = self.methods
        unique_types = set((method.name_type for method in methods))

        if len(unique_types) > 1:

            methods_to_product = []
            for unique_type in unique_types:
                selected_method_type = [method for method in methods if method.name_type == unique_type]
                methods_to_product.append(selected_method_type)

            # return list(product(*methods_to_product))
            # return list(product(*methods_to_product))
            return methods_to_product

        else:
            # return iter(methods)
            return methods
