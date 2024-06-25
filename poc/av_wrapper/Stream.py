from abc import ABC
from dataclasses import dataclass, field
from fractions import Fraction

from av.video.stream import VideoStream


@dataclass(kw_only=True)
class Stream:
    movie_path: str

    width: int | None = None
    height: int | None = None
    fps: Fraction | None = None
    pixel_format: str | None = None
    codec: str | None = None

    frame_counter: int = 0

