import copy
import json
from ast import literal_eval
from pathlib import PurePath

import numpy as np

from io_utils.utils import get_latest_file_from_directory
from speed_analyse_scripts.Measurement import Measurement, RawVelocity, MeasurementROI
from speed_analyse_scripts.Timer import Timer
from stitch.RegionOfInterest import RegionOfInterest
from stitch.rectify.FrameRectifier import FrameRectifier
from stitch.speed.VelocityEstimator import VelocityEstimator
from stitch.speed.VelocityFromFrames import VelocityFromFrames
from stitch.speed.regression.LstsqMethod import LstsqMethod


def init_movie_paths(config: dict) -> dict[str, str]:
    dir_paths = config["movies"]["movie"]
    extension = config["movies"]["extension"]

    files = {}
    for movie in dir_paths:
        files[movie["name"]] = get_latest_file_from_directory(movie["input"], extension)

    return files


def init_rectifier(config: dict) -> FrameRectifier:
    rectify_config_path = config["rectify_config"]
    with open(rectify_config_path, "r") as file:
        rectify_config = json.load(file)

    frame_size = literal_eval(config["frame_size"])
    frame_rectifier = FrameRectifier(rectify_config, *frame_size)
    frame_rectifier.calc_maps()

    return frame_rectifier


def init_velocity_rois(config: dict) -> dict[str, RegionOfInterest]:
    source_region_size = literal_eval(config["frame_size"])

    rois = {}
    for velocity_roi in config["velocity_roi"]:
        name, size = list(velocity_roi.items())[0]
        size = literal_eval(size)
        rois[name] = RegionOfInterest(source_region_size, *size)

    return rois


def init_raw_velocities(movie_paths: dict[str, str], velocity_rois: dict[str, RegionOfInterest]) -> list[RawVelocity]:
    result = []

    for movie_name in movie_paths.keys():
        for roi_name, roi in velocity_rois.items():
            item = RawVelocity(movie_name, roi_name, roi, VelocityFromFrames(), np.zeros((1, 3)))
            result.append(item)

    return result


def init_measurements(movie_paths: dict[str, str], velocity_estimators: dict[str, VelocityEstimator],
                      raw_velocities: list[RawVelocity]) -> list[MeasurementROI]:
    measurements = []
    for movie_name in movie_paths.keys():
        for method_name, estimator in velocity_estimators.items():
            for raw_velocity in raw_velocities:
                velocity_estimator = copy.deepcopy(estimator)

                measurement = MeasurementROI(movie_name, method_name, velocity_estimator, [], Timer(),
                                             raw_velocity.roi_name)
                measurements.append(measurement)

    return measurements
