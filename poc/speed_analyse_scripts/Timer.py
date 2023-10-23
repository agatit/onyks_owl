import time

import numpy as np


class Timer:
    def __init__(self):
        self.start_time = 0
        self._elapsed_time = []

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> None:
        elapsed_time = time.time() - self.start_time
        self._elapsed_time.append(elapsed_time)

    @property
    def elapsed_time(self):
        return np.mean(self._elapsed_time)
