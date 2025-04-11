from pydantic import BaseModel


class RectificationConfig(BaseModel):
    sensor_h: float
    sensor_w: float
    X: float
    Y: float
    alpha: float
    beta: float
    gamma: float
    focus: float
    scale: float
    dist: list[float]
