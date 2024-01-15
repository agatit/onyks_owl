import math
from abc import ABC, abstractmethod
from typing import Callable

import cv2
import numpy as np
from scipy.optimize import OptimizeResult

from rectify_optimalization.objective_functions.methods.Method import Method


class ObjectiveFunction(ABC):

    def __init__(self, consts: dict, *methods: Method):
        self.consts = consts
        self.methods = methods

    @abstractmethod
    def _aggregate_method(self, method_result: np.ndarray) -> float:
        pass

    def get_function_to_optimize(self) -> Callable[[list], float]:
        def wrapper(x):
            results = []

            for method in self.methods:
                rectified = self.rectify_lines(x, self.consts, method.lines)
                method_result = method.calculate(rectified)
                result = self._aggregate_method(method_result)

                result *= method.weight
                results.append(result)

            return sum(results)

        return wrapper

    @classmethod
    def rectify_lines(cls, config, consts, lines):
        result = np.zeros(lines.shape)

        for index, points in enumerate(lines):
            result[index] = cls.rectify_points(config, consts, points)

        return result

    @staticmethod
    def rectify_points(config, consts, points):
        sensor_h = config[0]
        sensor_w = config[1]
        X = config[2]
        Y = config[3]
        alpha = config[4]
        beta = config[5]
        gamma = config[6]
        focus = config[7]
        scale = config[8]
        dist = np.array(config[9:])

        W = consts["width"]
        H = consts["height"]

        Rx = np.array([[1, 0, 0], [0, math.cos(alpha), -math.sin(alpha)], [0, math.sin(alpha), math.cos(alpha)]])
        Ry = np.array([[math.cos(beta), 0, -math.sin(beta)], [0, 1, 0], [math.sin(beta), 0, math.cos(beta)]])
        Rz = np.array([[math.cos(gamma), -math.sin(gamma), 0], [math.sin(gamma), math.cos(gamma), 0], [0, 0, 1]])
        R = np.matmul(Rx, np.matmul(Ry, Rz))

        K = np.array([
            [W * focus / sensor_w, 0, W // 2],
            [0, H * focus / sensor_h, H // 2],
            [0, 0, 1]])
        new_K = np.array([
            [W * focus / sensor_w, 0, scale * W // 2 + X, 0],
            [0, H * focus / sensor_h, scale * H // 2 + Y, 0],
            [0, 0, 1, 0]])

        res = cv2.undistortPoints(points, K, dist, R=R, P=new_K)
        return np.reshape(res, (-1, 2))

    @staticmethod
    def make_rectify_config(optimize_result: OptimizeResult) -> dict:
        x = optimize_result.x

        return {
            'sensor_h': x[0],
            'sensor_w': x[1],
            'X': x[2],
            'Y': x[3],
            'alpha': x[4],
            'beta': x[5],
            'gamma': x[6],
            'focus': x[7],
            'scale': x[8],
            'dist': x[9:].tolist()
        }
