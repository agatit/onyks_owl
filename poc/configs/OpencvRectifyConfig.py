from functools import reduce

import cv2
from pydantic import BaseModel, Field


class Cache(BaseModel):
    obj_points: list
    img_points: list


class CameraConfig(BaseModel):
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float


class Criteria(BaseModel):
    flags: list[str] = Field(default_factory=list)
    iterations: int
    epsilon: float

    def to_cv2_criteria_tuple(self) -> tuple[int, int, float]:
        mask = load_cv2_bitmask(self.flags)
        return mask, self.iterations, self.epsilon


class GatherPointsConfig(BaseModel):
    enable: bool
    save_cache: bool
    chessboard_size: tuple[int, int]
    skip_frames: int
    workers: int
    findChessboardCorners_flags: list[str] = Field(default_factory=list)
    cornerSubPix_criteria: Criteria


class CalibrateCameraConfig(BaseModel):
    criteria: Criteria
    distCoeffs: list[float]
    flags: list[str]


class RectifyConfig(BaseModel):
    enable: bool
    skip_frames: int


class RotateConfig(BaseModel):
    enable: bool
    minimize_kwargs: dict
    init: dict
    bounds: dict


class OpencvRectifyConfig(BaseModel):
    camera: CameraConfig
    generate_mapx_mapy: bool
    rotate: RotateConfig
    rectify: RectifyConfig
    gather_points: GatherPointsConfig
    calibrateCamera: CalibrateCameraConfig
    getOptimalNewCameraMatrix: dict


def load_cv2_bitmask(str_flags: list[str]) -> int:
    if len(str_flags) < 1:
        return None

    int_flags = [getattr(cv2, str_flag) for str_flag in str_flags]
    return reduce(lambda a, b: a | b, int_flags)
