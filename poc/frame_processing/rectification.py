import numpy as np

from stitch.rectify.FrameRectifier import FrameRectifier


def rectify_batch_frames(batch: list[np.ndarray], frame_rectifier: FrameRectifier) -> np.ndarray:
    return [frame_rectifier.rectify(frame) for frame in batch]
