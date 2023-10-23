from dataclasses import dataclass

import numpy as np

from speed_analyse_scripts.Timer import Timer
from stitch.RegionOfInterest import RegionOfInterest
from stitch.speed.VelocityEstimator import VelocityEstimator
from stitch.speed.VelocityFromFrames import VelocityFromFrames


@dataclass
class Measurement:
    dataset_name: str
    method_name: str
    velocity_estimator: VelocityEstimator
    results: list[tuple]
    timer: Timer


@dataclass
class MeasurementROI(Measurement):
    roi_name: str


@dataclass
class RawVelocity:
    dataset_name: str
    roi_name: str
    roi: RegionOfInterest
    velocity_from_frames: VelocityFromFrames
    results: np.ndarray

    def append_velocity(self, frame):
        raw_velocity = self.velocity_from_frames.next(frame)
        self.results = np.vstack((self.results, raw_velocity))
