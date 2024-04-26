import copy
from dataclasses import dataclass, field

from label_selector.saving.Checkpoint import Checkpoint


@dataclass
class SaveManager:
    dataset_name: str
    _checkpoints: dict[str, Checkpoint] = field(init=False, default_factory=dict)

    def add_checkpoint(self, checkpoint: Checkpoint):
        checkpoint = copy.deepcopy(checkpoint)
        full_name = f"{self.dataset_name}_{checkpoint.name}"

        checkpoint.change_name(full_name)
        self._checkpoints[full_name] = checkpoint

    def get_checkpoint(self, name: str) -> Checkpoint:
        if name in self._checkpoints:
            return self._checkpoints[name]
        else:
            return None

    def get_latest_checkpoint(self) -> Checkpoint:
        checkpoints = [i for i in self._checkpoints.values()
                       if i.full_path.exists() and i.full_path.stat().st_size > 0]

        if len(checkpoints) > 0:
            checkpoints.sort(key=lambda c: c.full_path.stat().st_mtime)
            return checkpoints.pop()
        else:
            return None

    def get_names(self) -> list[str]:
        return self._checkpoints.keys()

    def get_checkpoints(self) -> list[Checkpoint]:
        return list(self._checkpoints.values())
