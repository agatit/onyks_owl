from dataclasses import dataclass

from label_selector.ProcessData import ProcessData


@dataclass
class Checkpoint:
    current_index: int
    process_data: list[ProcessData]

    @classmethod
    def from_pickle(cls, **kwargs):
        current_index = kwargs['current_index']
        process_data = [ProcessData(i["image_path"], i["label_rectangles"]) for i in kwargs["process_data"]]
        return cls(current_index, process_data)
