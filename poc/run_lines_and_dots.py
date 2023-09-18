import json
from dataclasses import dataclass
from enum import Enum

import click
import cv2

from lines_and_dots.image_event_handler import ImageEventHandler


@dataclass
class LineType:
    type: str
    max_dots_number: int
    lines: list


class PressedKey(Enum):
    escape = 27
    space = 32
    enter = 13
    tab = 9


def scale_shape_by_percent(shape, percent):
    width = int(shape[1] * percent / 100)
    height = int(shape[0] * percent / 100)
    return width, height


def scale_point_by_percent(point, percent):
    y = int(point[1] * percent / 100)
    x = int(point[0] * percent / 100)
    return x, y


@click.command()
@click.argument("input_file")
@click.option("-o", "--output", "output_file", default="lines.json", help="output json file")
@click.option("-dn", "--dots_number", "max_dots_number", default=-1, help="number of output line dots")
def main(input_file, output_file, max_dots_number):
    image = cv2.imread(input_file)
    window_name = "image"
    resize_percent = {
        "scale_down": 75,
        "scale_up": 133,
    }

    original_image = image.copy()
    down_scaled_dim = scale_shape_by_percent(image.shape, resize_percent["scale_down"])
    image = cv2.resize(image, down_scaled_dim, interpolation=cv2.INTER_AREA)

    horizontal_lines = LineType("horizontal", max_dots_number, [])
    vertical_lines = LineType("vertical", max_dots_number, [])
    image_event_handler = ImageEventHandler(image, window_name, horizontal_lines, vertical_lines)

    cv2.imshow(window_name, image)
    cv2.setMouseCallback(window_name, image_event_handler.mouse_callback())

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
                scaled_dot = scale_point_by_percent(dot, resize_percent["scale_up"])
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
        resize_map = lambda x: scale_point_by_percent(x, resize_percent["scale_up"])

        for line_type in image_event_handler.line_types:
            for i in range(len(line_type.lines)):
                line_type.lines[i] = list(map(resize_map, line_type.lines[i]))

        with open(output_file, "w") as file:
            dicts = []
            for line_type in image_event_handler.line_types:
                dicts.append(vars(line_type))

            json.dump(dicts, file)


if __name__ == '__main__':
    main()
