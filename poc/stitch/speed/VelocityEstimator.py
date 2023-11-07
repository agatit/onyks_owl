import copy
import dataclasses

import cv2
import numpy as np

from stitch.speed.RegressionModel import RegressionModel
from stitch.speed.VelocityFromFrames import VelocityFromFrames
from stitch.speed.regression.Method import Method


class VelocityEstimator:
    x_max_velocity = 75
    y_max_velocity = 2

    x_max_change_velocity = 5
    y_max_change_velocity = 2

    def __init__(self, regression_model_x: Method, regression_model_y: Method, window_size=25, center=True):
        self.x_regression_model = regression_model_x
        self.y_regression_model = regression_model_y
        self.window_size = window_size
        self.center = center

        self.velocity_from_frames = VelocityFromFrames()

        self.window = np.array([[0, 0, 0]])
        self.old_raw_velocity = np.array([[0, 0, 0]])
        self.last_velocity = (0, 0)
        self.frames_counter = 0

        self.frame_index = 0
        if center:
            self.get_frame_index = self._get_middle_frame_index
        else:
            self.get_frame_index = self.__get_last_frame_index

        self.old_frame = None

    def get_velocity(self, frame):
        self._update_window(frame)
        self._update_regression_model()

        if len(self.window) > 0:
            self.frame_index = self.get_frame_index()
            x = self.x_regression_model.predict(self.frame_index)
            y = self.y_regression_model.predict(self.frame_index)

            if self.window_size < self.frames_counter:
                x, y = self._filter_outliers(x, y)

            self.last_velocity = (x, y)
            return x, y
        else:
            return self.last_velocity

    def _filter_outliers(self, x, y):
        last_x, last_y = self.last_velocity
        if abs(x - last_x) > self.x_max_change_velocity:
            x = self.last_velocity[0]

        if abs(y - last_y) > self.y_max_change_velocity:
            y = self.last_velocity[1]

        return x, y

    def _update_window(self, frame):
        raw_velocity = self.velocity_from_frames.next(frame)

        if len(self.window) < 1:
            self.__reload_window()

        self.window = np.vstack((self.window, raw_velocity))

        if self.window_size < self.frames_counter and len(self.window) > self.window_size:
            self._remove_first_frame()

        self.old_raw_velocity = raw_velocity
        self._update_frames_counter()

    def _update_regression_model(self):
        window = self.window
        frame = window[:, 0]
        x = window[:, 1]
        y = window[:, 2]

        self.x_regression_model.fit(frame, x)
        self.y_regression_model.fit(frame, y)

    def _remove_first_frame(self):
        window = self.window

        min_frame = window[:, 0].min()
        condition_min = window[:, 0] > min_frame

        self.window = window[condition_min]

    def _update_frames_counter(self):
        self.frames_counter += 1

    def _get_middle_frame_index(self):
        window = self.window[:, 0]
        middle_index = len(window) // 2
        return window[middle_index]

    def __get_last_frame_index(self):
        return self.window[:, 0].max()

    def __reload_window(self):
        self.window = np.array([[0, 0, 0]])
