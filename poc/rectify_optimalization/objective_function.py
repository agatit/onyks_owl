import math

import cv2
import numpy as np

from rectify_optimalization.distance import calc_distance
from rectify_optimalization.objective_functions.methods import Method


def rectify_points(config, consts, points):
    X = config[0]
    Y = config[1]
    alpha = config[2]
    beta = config[3]
    gamma = config[4]
    focus = config[5]
    scale = config[6]
    dist = config[7:]

    W = consts["W"]
    H = consts["H"]
    sensor_w = consts["sensor_w"]
    sensor_h = consts["sensor_h"]

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


def rectify_lines(config, consts, lines):
    result = np.zeros(lines.shape)

    for index, points in enumerate(lines):
        result[index] = rectify_points(config, consts, points)

    return result


def calc_horizontal_std(config, consts, horizontal) -> np.ndarray:
    horizontal_rectified = rectify_lines(config, consts, horizontal)
    return horizontal_rectified[:, :, 1].std(axis=1)


def calc_vertical_std(config, consts, vertical) -> np.ndarray:
    vertical_rectified = rectify_lines(config, consts, vertical)
    return vertical_rectified[:, :, 0].std(axis=1)


def calc_horizontal_distance(config, consts, horizontal) -> np.ndarray:
    distances_rectified = rectify_lines(config, consts, horizontal)
    return calc_distance(distances_rectified[:, :, 0])


def calc_rectified(config, consts, line, method: Method):
    rectified = rectify_lines(config, consts, line)
    return method.calculate(None)

def objective_function(x, consts, horizontal, vertical, distances):
    horizontal_std = calc_horizontal_std(x, consts, horizontal)
    vertical_std = calc_vertical_std(x, consts, vertical)
    horizontal_distance = calc_horizontal_distance(x, consts, distances)

    weights = consts["weights"]
    stds = weights["std"] * (horizontal_std.mean() + vertical_std.mean())
    distance = weights["distance"] * horizontal_distance.mean()

    return stds + distance
