import json
from dataclasses import dataclass

from stream.commands.export.Exporter import Exporter


@dataclass
class JsonExporter(Exporter):
    dict_to_dump: dict

    def execute(self) -> None:
        with open(self.output_path, "w") as file:
            json.dump(self.dict_to_dump, file)
