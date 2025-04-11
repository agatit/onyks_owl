import os
import random
import tempfile
from dataclasses import dataclass, field
from itertools import cycle
from logging import Logger
from pathlib import Path
from typing import Protocol, Callable
from PIL import Image
import cv2
import numpy as np
from sympy.physics.units import radian

from display.utils import scale_point_by_percent, scale_image_by_percent
from rectify_lines.LineType import LineType
from rectify_lines.OpencvWindow import OpencvWindow


@dataclass(kw_only=True)
class AppContext:
    close_app = False
    export_flag = False

    line_types: list[LineType]

    dots: list[tuple[int, int]] = field(init=False, repr=False, default_factory=list)

    def __post_init__(self):
        self.line_types_cycle = cycle(self.line_types)
        self.current_line_type = next(self.line_types_cycle)

    def save_current_dots(self):
        self.current_line_type.lines.append(self.dots)
        self.reload()

    def reload(self):
        self.dots = []


class EventManager:
    def __init__(self):
        self._events: dict[str, list[Callable]] = {}

    def add_event(self, name: str, func: Callable) -> None:
        if name not in self._events:
            self._events[name] = []

        self._events[name].append(func)

    def notify(self, name: str) -> None:
        if name not in self._events:
            return

        for func in self._events[name]:
            func()


def log_status(app_context: AppContext, logger: Logger):
    logger.info(f"Current Line Type: {app_context.current_line_type.type}")
    for line_type in app_context.line_types:
        logger.info(f"{line_type.type}: {len(line_type.lines)}")


def append_dots(app_context: AppContext, image_window: OpencvWindow):
    x = image_window.last_mouse_event.x
    y = image_window.last_mouse_event.y

    if len(app_context.dots) < app_context.current_line_type.max_dots_number:
        app_context.dots.append((x, y))
        image_window.paint_dot(x, y)
    else:
        app_context.reload()
        image_window.reload()

    # print(app_context.dots)


def next_line_type(app_context: AppContext, image_window: OpencvWindow):
    app_context.current_line_type = next(app_context.line_types_cycle)

    app_context.reload()
    image_window.reload()

def save_line(app_context: AppContext, image_window: OpencvWindow):
    if len(app_context.dots) == app_context.current_line_type.max_dots_number:
        app_context.save_current_dots()
    else:
        app_context.reload()

    image_window.reload()


def display_all_dots(
        app_context: AppContext,
        image_window: OpencvWindow,
        resize_percent: int
):
    preview_image = scale_image_by_percent(image_window.img, resize_percent)
    preview_window = OpencvWindow("preview", preview_image)

    radius = preview_window.PAINT_DOT_KWARGS["radius"]
    thickness = preview_window.PAINT_DOT_KWARGS["thickness"]

    for line_type in app_context.line_types:
        for line in line_type.lines:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for dot in line:
                scaled_dot = scale_point_by_percent(dot, resize_percent)
                # content
                cv2.circle(
                    img=preview_image,
                    center=scaled_dot,
                    radius=radius,
                    thickness=thickness,
                    color=color
                )

                # border
                cv2.circle(
                    img=preview_image,
                    center=scaled_dot,
                    radius=radius,
                    thickness=1,
                    color=(0, 0, 0)
                )

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir_name = Path(tmp_dir_name)
        tmp_img = tmp_dir_name / "preview.png"
        cv2.imwrite(tmp_img, preview_image)

        im = Image.open(tmp_img)
        im.show()


def close_app(app_context: AppContext):
    app_context.close_app = True


def set_export_flag(app_context: AppContext):
    app_context.export_flag = True

# def refresh_status_window(app_context: AppContext, status_window: OpencvWindow):
#     app_context.close_app = False
