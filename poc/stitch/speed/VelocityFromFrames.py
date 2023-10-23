import copy

import cv2
import numpy as np

debug = True


class VelocityFromFrames:
    def __init__(self, y_max_velocity=2, x_min_velocity=1, x_max_velocity=75, window=50):
        # params for ShiTomasi corner detection
        self.feature_params = dict(maxCorners=100,
                                   qualityLevel=0.02,
                                   minDistance=50,
                                   blockSize=14)

        # Parameters for lucas kanade optical flow
        self.lk_params = dict(winSize=(x_max_velocity + 3, y_max_velocity + 3),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.01))

        self.y_max_velocity = y_max_velocity
        self.x_min_velocity = x_min_velocity
        self.window = window

        self.frames_counter = 0
        self.input_frame_shape = (0, 0, 0)
        self.old_frame = None

        self.points0 = np.zeros((1, 2))
        self.points1 = np.zeros((1, 2))
        self.status = np.zeros(1, )
        self.filter = np.array([True])

        self.old_velocity = np.array([[0, 0, 0]])

    def next(self, frame):
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.old_frame is None:
            self.input_frame_shape = frame.shape
            self.old_frame = grayscale_frame
            self.__update_frames_counter()
            return self.old_velocity

        points0 = cv2.goodFeaturesToTrack(self.old_frame, mask=None, **self.feature_params)
        points1, status, err = cv2.calcOpticalFlowPyrLK(self.old_frame, grayscale_frame, points0, None, **self.lk_params)
        self.old_frame = grayscale_frame

        points0 = points0[:, 0]
        points1 = points1[:, 0]
        status = status[:, 0]

        self.points0 = points0
        self.points1 = points1
        self.status = status

        velocities = points1 - points0

        con_status = status == 1
        con_max_y_change = np.abs(velocities[:, 1]) < self.y_max_velocity
        con_max_x_change = np.abs(velocities[:, 0]) > self.x_min_velocity
        self.filter = con_status & con_max_y_change & con_max_x_change
        # self.filter = con_status & con_max_y_change
        velocities = velocities[self.filter]

        n = len(velocities)
        index_col = np.full(n, self.frames_counter).reshape(n, 1)
        index_velocities = np.hstack((index_col, velocities))

        self.old_velocity = copy.deepcopy(index_velocities)
        self.__update_frames_counter()
        return index_velocities

    def draw_point_from_last_record(self):
        draw_points = np.zeros(self.input_frame_shape).astype(np.uint8)

        # wszyskie
        for (p0, p1) in zip(self.points0, self.points1):
            draw_points = cv2.circle(draw_points, p0.astype(int), 5, (0, 0, 255), -1)

        # dobre
        points0 = self.points0[self.filter]
        points1 = self.points1[self.filter]
        for (p0, p1) in zip(points0, points1):
            draw_points = cv2.circle(draw_points, p0.astype(int), 5, (0, 255, 0), -1)
            draw_points = cv2.line(draw_points, p0.astype(int), p1.astype(int), (255, 0, 0), 2)

        return draw_points

    def __update_frames_counter(self):
        self.frames_counter += 1
