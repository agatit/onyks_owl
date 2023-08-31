import json
from dataclasses import dataclass
from enum import Enum

import click
import cv2

from image_event_handler import ImageEventHandler


@dataclass
class LineType:
    type: str
    lines: list


class PressedKey(Enum):
    escape = 27
    space = 32
    enter = 13
    tab = 9


def scale_image_by_percent(image, percent):
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


@click.command()
@click.argument("file_path")
@click.option("-o", "--output", "output_file", default="lines.json")
def main(file_path, output_file):
    image = cv2.imread(file_path)
    window_name = "image"
    resize_percent = {
        "scale_down": 75,
        "scale_up": 133,
    }

    original_image = image.copy()
    image = scale_image_by_percent(image, resize_percent["scale_down"])

    horizontal_lines = LineType("horizontal", [])
    vertical_lines = LineType("vertical", [])
    image_event_handler = ImageEventHandler(image, window_name, horizontal_lines, vertical_lines)

    cv2.imshow(window_name, image)
    cv2.setMouseCallback(window_name, image_event_handler.mouse_callback())

    image_event_handler.display_current_line_type()

    while True:
        key = cv2.waitKey(0)

        # check if window still exists
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            break

        if key == PressedKey.enter.value:
            break

        if key == PressedKey.space.value:
            image_event_handler.save_current_dots()
            image_event_handler.display_current_line_type()

            line_types = image_event_handler.line_types
            print()
            for line_type in line_types:
                print(f"{line_type.type}: {line_type.lines}")

        if key == PressedKey.tab.value:
            img = original_image.copy()
            dots = image_event_handler.dots

            for dot in dots:
                x, y = dot

                scale_up = resize_percent["scale_up"]
                width = int(x * scale_up / 100)
                height = int(y * scale_up / 100)
                dim = (width, height)

                circle_kwargs = {
                    "img": img,
                    "center": dim,
                    "radius": 5,
                    "thickness": -1,
                    "color": (0, 255, 255)
                }

                cv2.circle(**circle_kwargs)

            cv2.imshow('original', img)

    cv2.destroyAllWindows()

    with open(output_file, "w") as file:
        dicts = []
        for line_type in image_event_handler.line_types:
            dicts.append(vars(line_type))

        json.dump(dicts, file)


if __name__ == '__main__':
    main()
