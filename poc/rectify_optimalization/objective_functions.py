from typing import Protocol

import cv2
import numpy as np

from rectify_optimalization.methods.Method import Method


class ObjectiveFunction(Protocol):
    def __call__(self, x: list[float]) -> float:
        pass


def rotation_function(
        x: list[float],
        methods: list[Method],
        camera_matrix: np.ndarray,
        dist: np.ndarray,
        new_camera_matrix: np.ndarray
) -> float:
    results = []

    R, _ = cv2.Rodrigues(np.array(x))

    for method in methods:
        rectified_lines = []
        for line in method.lines:
            rectified_line = cv2.undistortPoints(
                src=line,
                R=R,
                cameraMatrix=camera_matrix,
                distCoeffs=dist,
                P=new_camera_matrix
            )
            rectified_line = np.reshape(rectified_line, (-1, 2))
            rectified_lines.append(rectified_line)

        rectified_lines = np.array(rectified_lines)
        result = method.calculate(rectified_lines).mean().sum()
        results.append(result)

    return sum(results) / len(results)
