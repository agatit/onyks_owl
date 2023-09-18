import copy

import cv2
import time
import logging
from statistics import median
import numpy as np

debug = True


class CarSpeedEstimator:
    def __init__(
            self,
            y_max_velocity=2,
            x_min_velocity=5,
            x_max_velocity=75,
            window=50
    ):

        # constants
        # params for ShiTomasi corner detection
        self.feature_params = dict(maxCorners=100,
                                   qualityLevel=0.02,
                                   minDistance=50,
                                   blockSize=14)
        # Parameters for lucas kanade optical flow
        self.lk_params = dict(winSize=(x_max_velocity + 3, y_max_velocity + 3),
                              # TODO: 3 to minimum, do przemyślenia!!!
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.01))

        self.y_max_velocity = y_max_velocity
        self.x_min_velocity = x_min_velocity
        self.window = window

        self.old_frame = None
        self.velocity_history = np.empty((0, 2), dtype=np.float64)
        print(self.velocity_history.shape)

    def next(self, frame, pts=1 / 30, debug=None):
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.old_frame is None:
            self.old_frame = frame
            return (0, 0), debug, np.array([(0, 0)])

        points0 = cv2.goodFeaturesToTrack(self.old_frame, mask=None, **self.feature_params)
        points1, status, err = cv2.calcOpticalFlowPyrLK(self.old_frame, frame, points0, None, **self.lk_params)
        raw_status = copy.deepcopy(status)

        # warotści goodFeaturesToTrack i calcOpticalFlowPyrLK mają zbędny 2-gi wymiar - usuwamy
        points0 = points0[:, 0]
        points1 = points1[:, 0]
        status = status[:, 0]

        velocities = points1 - points0
        raw_velocities = copy.deepcopy(velocities)
        raw_velocities = np.append(raw_velocities, raw_status, axis=1)

        # eliminacja nieporuszających się, lub poruszjących w pionie
        status = (status == 1) \
                 & (np.abs(velocities[:, 1]) < self.y_max_velocity) \
                 & (np.abs(velocities[:, 0]) > self.x_min_velocity)

        velocities = velocities[status]
        # raw_velocities = copy.deepcopy(velocities)

        # debug
        if debug is not None:
            # wszyskie
            for (p0, p1) in zip(points0, points1):
                debug = cv2.circle(debug, p0.astype(int), 5, (0, 0, 255), -1)
                # debug = cv2.line(debug, p0.astype(int), p1.astype(int), (255,0,0), 2)
            # dobre
            points0 = points0[status]
            points1 = points1[status]
            for (p0, p1) in zip(points0, points1):
                debug = cv2.circle(debug, p0.astype(int), 5, (0, 255, 0), -1)
                debug = cv2.line(debug, p0.astype(int), p1.astype(int), (255, 0, 0), 2)

        self.old_frame = frame

        # odrzucanie błedów grubych        
        if len(velocities) > 0:
            perc_low = np.percentile(velocities[:, 0], 20)
            perc_high = np.percentile(velocities[:, 0], 80)
            self.velocity_history = np.append(self.velocity_history, velocities[(velocities[:, 0] >= perc_low) & (
                    velocities[:, 0] <= perc_high), :], axis=0)

        # obliczenia z uwzględnieniem historii
        if len(self.velocity_history) > 0:
            # ponowne odrzucanie błedów grubych, 
            perc_low = np.percentile(self.velocity_history[:, 0], 20)
            perc_high = np.percentile(self.velocity_history[:, 0], 80)
            to_avarage = self.velocity_history[
                (self.velocity_history[:, 0] >= perc_low) & (self.velocity_history[:, 0] <= perc_high)]

            # uśrednanie
            if len(to_avarage) > 0:
                velocity_avg_x = np.average(to_avarage[:, 0])
                velocity_avg_y = np.average(to_avarage[:, 1])
            else:
                velocity_avg_x = np.average(self.velocity_history[:, 0])
                velocity_avg_y = np.average(self.velocity_history[:, 1])

            # przycinanie historii
            if self.window < len(self.velocity_history):
                self.velocity_history = self.velocity_history[-self.window:]
            else:
                self.velocity_history = np.delete(self.velocity_history, 0, axis=0)
        else:
            velocity_avg_x = 0
            velocity_avg_y = 0

        return (velocity_avg_x, velocity_avg_y), debug, raw_velocities

