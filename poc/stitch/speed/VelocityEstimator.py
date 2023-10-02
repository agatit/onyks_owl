import copy
import dataclasses

import cv2
import numpy as np

from stitch.speed.RegressionModel import RegressionModel
from stitch.speed.regression.Method import Method


class VelocityEstimator:
    x_max_velocity = 75
    y_max_velocity = 2

    feature_params = dict(maxCorners=100,
                          qualityLevel=0.02,
                          minDistance=50,
                          blockSize=14)

    lk_params = dict(winSize=(x_max_velocity + 3, y_max_velocity + 3),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.01))

    def __init__(self, regression_model_x: Method, regression_model_y: Method, window_size=25, center=True):
        self.x_regression_model = regression_model_x
        self.y_regression_model = regression_model_y
        self.window_size = window_size
        self.center = center

        self.window = np.array([[0, 0, 0]])
        self.old_raw_velocity = np.array([[0, 0, 0]])
        self.frames_counter = 0

        if center:
            self.get_frame = self.get_middle_frame
        else:
            self.get_frame = self.get_last_frame

        self.old_frame = None

    def get_velocity(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.old_frame is None:
            self.old_frame = frame
            self.update_frames_counter()
            return 0, 0

        self.update_window(frame)
        self.update_regression_model()

        frame_to_predict = self.get_frame()
        x = self.x_regression_model.predict(frame_to_predict)
        y = self.y_regression_model.predict(frame_to_predict)
        return x, y

    def update_window(self, frame):
        raw_velocity = self.get_raw_velocity(frame)
        self.window = np.vstack((self.window, raw_velocity))

        if self.window_size < self.frames_counter:
            self.remove_first_last_frame()

        self.update_frames_counter()

    def update_regression_model(self):
        window = self.window
        frame = window[:, 0]
        x = window[:, 1]
        y = window[:, 2]

        self.x_regression_model.fit(frame, x)
        self.y_regression_model.fit(frame, y)

    def remove_first_last_frame(self):
        window = self.window

        min_frame = window[:, 0].min()
        # max_frame = window[:, 0].max()

        condition_min = window[:, 0] > min_frame
        # condition_max = window[:, 0] < max_frame

        self.window = window[condition_min]
        # self.window = window[condition_min & condition_max]
        # print(np.unique(self.window[:, 0]))

    def get_raw_velocity(self, frame):
        points0 = cv2.goodFeaturesToTrack(self.old_frame, mask=None, **self.feature_params)
        points1, status, err = cv2.calcOpticalFlowPyrLK(self.old_frame, frame, points0, None, **self.lk_params)
        self.old_frame = frame

        points0 = points0[:, 0]
        points1 = points1[:, 0]
        status = status[:, 0]

        velocities = points1 - points0

        con_status = status == 1
        con_max_y_change = np.abs(velocities[:, 1]) < self.y_max_velocity
        velocities = velocities[con_status & con_max_y_change]

        n = len(velocities)
        index_col = np.full(n, self.frames_counter).reshape(n, 1)
        index_velocities = np.hstack((index_col, velocities))

        self.old_raw_velocity = copy.deepcopy(index_velocities)
        return index_velocities

    def update_frames_counter(self):
        self.frames_counter += 1

    def get_middle_frame(self):
        window = self.window[:, 0]
        middle_index = len(window) // 2
        return window[middle_index]

    def get_last_frame(self):
        return self.window[:, 0].max()
