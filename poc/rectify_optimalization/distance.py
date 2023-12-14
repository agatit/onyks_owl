from itertools import tee

import numpy as np


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))


def middle_value(array):
    length = array.shape[1]

    if length % 2 == 0:
        upper_index = length // 2
        lower_index = upper_index - 1
        return (array[:, lower_index] + array[:, upper_index]) / 2
    else:
        middle_index = length // 2
        return array[:, middle_index]


def deviation(array, mean_array):
    x = abs(array - mean_array) ** 2
    return np.sqrt(np.mean(x, 1))


def calc_distance(array):
    x = np.apply_along_axis(pairwise, 1, array)
    x = np.abs(x[:, :, 0] - x[:, :, 1])
    return x.std(axis=1)
