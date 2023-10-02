import csv
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CsvData:
    headers: list
    data: list[tuple]

    @staticmethod
    def timestamp_output_file():
        time = datetime.now().strftime("%Y%m%dT%H%M%S")
        return time + ".csv"


def export(file, cvs_data: CsvData):
    writer = csv.writer(file)

    writer.writerow(cvs_data.headers)
    for data in cvs_data.data:
        writer.writerow(data)
