import json
from dataclasses import dataclass, field

import cv2
import numpy as np



@dataclass
class Measurement:
    name: str
    lines_file_path: str
    image_path: str
    horizontal_lines: np.ndarray = field(init=False)
    vertical_lines: np.ndarray = field(init=False)

    def __post_init__(self):
        self.horizontal_lines = np.array([])
        self.vertical_lines = np.array([])

    def load_image(self) -> np.ndarray:
        return cv2.imread(self.image_path)

    def load_lines(self) -> None:
        with open(self.lines_file_path, "r") as file:
            lines = json.load(file)

        self.horizontal_lines = np.array(lines[0]["lines"], dtype=np.float64)
        self.vertical_lines = np.array(lines[1]["lines"], dtype=np.float64)


