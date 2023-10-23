import csv
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO

import numpy as np


@dataclass
class CsvData:
    headers: list
    data: list[tuple]


def ndarray_to_list_tuple(array: np.ndarray) -> list[tuple]:
    return [tuple(i) for i in array]


def to_csv(file: TextIO, cvs_data: CsvData):
    writer = csv.writer(file)

    writer.writerow(cvs_data.headers)
    for data in cvs_data.data:
        writer.writerow(data)
