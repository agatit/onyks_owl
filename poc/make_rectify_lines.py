import ast
import dataclasses
import json
from typing import Union

import click
import cv2
import numpy as np

from display.OpenCVstyles import OpenCVstyles
from display.PressedKey import PressedKey
from display.RegionOfInterest import RegionOfInterest
from display.utils import scale_image_by_percent, scale_point_by_percent
from rectify_lines.ImageEventHandler import ImageEventHandler
from rectify_lines.LineType import LineType


@click.command()
@click.argument("input_file")
@click.option("-o", "--output", "output_file", type=click.Path(), default="lines.json",
              help="output json file")
@click.option("-dn", "--dots_number", "max_dots_number", default=-1, help="number of output line dots")
@click.option("-sc", "--scale", "scale", default=75, help="scale image to display")
@click.option("-roi", "--region", "roi_str", help="format: [x1,y1,x2,y2]")
def main(input_file, output_file, max_dots_number, scale, roi_str):
    image = cv2.imread(input_file)
    window_name = "image"
    resize_percent = {
        "scale": scale,
        "scale_back": 100 // (scale / 100),
    }

    try:
        roi = init_roi(image, roi_str)
    except SyntaxError:
        raise Exception("invalid roi string")

    image = cv2.rectangle(image, roi.p1, roi.p2, **OpenCVstyles.roi_rectangle.value)

    original_image = image.copy()
    image = scale_image_by_percent(image, resize_percent["scale"])

    lines = LineType("horizontal", max_dots_number, roi)
    vertical_lines = LineType("vertical", max_dots_number, roi)
    image_event_handler = ImageEventHandler(image, window_name, lines, vertical_lines)

    cv2.imshow(window_name, image)
    cv2.setMouseCallback(window_name, image_event_handler.get_mouse_callback())

    image_event_handler.display_line_type_state()

    check_if_save = False
    while True:
        key = cv2.waitKey(0)

        # check if window still exists
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            break

        if key == PressedKey.escape.value:
            break

        if key == PressedKey.enter.value:
            check_if_save = True
            break

        if key == PressedKey.space.value:
            image_event_handler.save_current_dots()
            image_event_handler.display_line_type_state()

            line_types = image_event_handler.line_types
            print()
            for line_type in line_types:
                print(f"{line_type.type}: {line_type.lines}")

        if key == PressedKey.tab.value:
            img = original_image.copy()
            dots = image_event_handler.dots

            for dot in dots:
                scaled_dot = scale_point_by_percent(dot, resize_percent["scale_back"])
                circle_kwargs = {
                    "img": img,
                    "center": scaled_dot,
                    "radius": 5,
                    "thickness": -1,
                    "color": (0, 0, 255)
                }
                cv2.circle(**circle_kwargs)

            cv2.imshow('original', img)

    cv2.destroyAllWindows()

    if check_if_save:
        # scale up to input size
        resize_map = lambda x: scale_point_by_percent(x, resize_percent["scale_back"])

        for line_type in image_event_handler.line_types:
            for i in range(len(line_type.lines)):
                line_type.lines[i] = list(map(resize_map, line_type.lines[i]))

        with open(output_file, "w") as file:
            output = [generate_output(i) for i in image_event_handler.line_types]
            json.dump(output, file)


def init_roi(image: np.ndarray, roi_str: Union[None, str]) -> RegionOfInterest:
    image_height, image_width, _ = image.shape

    if roi_str:
        region_of_interest = ast.literal_eval(roi_str)
    else:
        region_of_interest = [0, 0, image_width, image_height]
    image_size = (image_width, image_height)

    return RegionOfInterest(image_size, *region_of_interest)


def generate_output(line_type: LineType) -> dict:
    new_output = dataclasses.asdict(line_type)
    new_output["roi"] = new_output["roi"].get_apices()
    return new_output


if __name__ == '__main__':
    main()
