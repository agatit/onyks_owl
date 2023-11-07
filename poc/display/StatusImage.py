import numpy as np


class StatusImage:

    def __init__(self, shape):
        self.background = np.full(shape, 255, dtype=np.uint8)
        self.background_copy = self.background.copy()

    def overlay(self, image):
        shape = self.background.shape
        image[:shape[0], :shape[1]] = self.background

    def reload(self):
        self.background = self.background_copy.copy()
