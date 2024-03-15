from dataclasses import dataclass

from label_selector.ProcessData import ProcessData


@dataclass
class Checkpoint:
    current_index: int
    process_data: list[ProcessData]
