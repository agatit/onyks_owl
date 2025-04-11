import ast
import json
from dataclasses import dataclass, field, asdict
from functools import partial
from typing import Union

import click
import cv2
import numpy as np
from rich.console import Console
from rich.table import Table

from display.OpenCVstyles import OpenCVstyles
from display.RegionOfInterest import RegionOfInterest
from display.utils import scale_image_by_percent, scale_point_by_percent
from loggers.loggers import init_rich_info_logger
from rectify_lines.LineType import LineType
from rectify_lines.OpencvWindow import OpencvWindow, MouseEvent
from rectify_lines.events import EventManager, AppContext, close_app, set_export_flag, next_line_type, append_dots, \
    save_line, display_all_dots, log_status

# from rectify_lines.events import EventManager

logger = init_rich_info_logger(__name__, format="%(message)s")

@dataclass
class KeyBinding:
    name: str
    event_names: list[str] = field(default_factory=list)
    description: str = field(default="")


keybindings: dict[int, KeyBinding] = {
    27: KeyBinding("Escape", ["exit_app"],
                   "Turn off an application without saving."),
    32: KeyBinding("Space", ["save_line", "log_status"],
                   "Save current dots as line. If dots' count does not match max dots' number, the result won't be saved."),
    13: KeyBinding("Enter", ["set_export", "exit_app"],
                   "Export Lines to file and exit application."),
    9: KeyBinding("Tab", ["display_all_dots"],
                  "Paint all dots in a separate window."),
    cv2.EVENT_LBUTTONDOWN: KeyBinding("LPM", ["append_dots"],
                                      "Add a dot to a line. If dots' count is bigger than max dots' number, the line will be reset."),
    cv2.EVENT_RBUTTONDOWN: KeyBinding("RPM", ["next_line_type", "log_status"],
                                      "Change a line type and reset current line."),
}


@click.command()
@click.option("-in", "--input", "input_file",
              required=True, type=click.Path(exists=True),
              help="select image to display")
@click.option("-o", "--output", "output_file",
              type=click.Path(), default="lines.json",
              help="output json file")
@click.option("-dn", "--dots_number", "max_dots_number",
              default=10, help="number of output line dots")
@click.option("-sc", "--scale", "scale",
              default=30, help="scale image to display")
@click.option("-roi", "--region", "roi_str",
              type=(int, int, int, int),
              help="select region of interest")
def main(input_file, output_file, max_dots_number, scale, roi_str):
    """
        Mark points of vertical or horizontal lines for a given image.
    """
    # print keybindings
    console = Console()
    table = Table(show_header=True)
    table.add_column("keybinding")
    table.add_column("description")
    for keybinding in keybindings.values():
        table.add_row(keybinding.name, keybinding.description)
    console.print(table)

    # init input image
    image = cv2.imread(input_file)
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

    windows_names = []

    # image window
    image_window_name = "image"
    windows_names.append(image_window_name)

    horizontal_lines = LineType("horizontal", max_dots_number, roi)
    vertical_lines = LineType("vertical", max_dots_number, roi)

    image_window = OpencvWindow("image", image)
    image_window.show()

    app_context = AppContext(
        line_types=[horizontal_lines, vertical_lines],
    )

    event_manager = EventManager()

    # global
    event_manager.add_event("log_status", partial(log_status, app_context, logger))

    # mouse
    event_manager.add_event("next_line_type", partial(next_line_type, app_context, image_window))
    event_manager.add_event("append_dots", partial(append_dots, app_context, image_window))

    # keyboard
    event_manager.add_event("exit_app", partial(close_app, app_context))
    event_manager.add_event("set_export", partial(set_export_flag, app_context))
    event_manager.add_event("save_line", partial(save_line, app_context, image_window))
    event_manager.add_event("display_all_dots",
                            partial(display_all_dots, app_context, image_window, resize_percent["scale_back"]))

    def mouse_callback(event_key, x, y, flags, userdata):
        if event_key in keybindings:
            image_window.last_mouse_event = MouseEvent(event_key, x, y, flags, userdata)

            for event_name in keybindings[event_key].event_names:
                event_manager.notify(event_name)

    cv2.setMouseCallback(image_window_name, mouse_callback)

    event_manager.notify("log_status")
    while True:
        if app_context.close_app:
            break

        # check if all windows still exist
        if not all(cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) for name in windows_names):
            break

        key = cv2.waitKey(0)

        if key in keybindings:
            for event_name in keybindings[key].event_names:
                event_manager.notify(event_name)

    cv2.destroyAllWindows()

    if app_context.export_flag:
        # scale up to input size
        resize_map = lambda x: scale_point_by_percent(x, resize_percent["scale_back"])

        for line_type in app_context.line_types:
            for i in range(len(line_type.lines)):
                line_type.lines[i] = list(map(resize_map, line_type.lines[i]))

        with open(output_file, "w") as file:
            output = [generate_output(i) for i in app_context.line_types]
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
    new_output = asdict(line_type)
    new_output["roi"] = new_output["roi"].get_apices()
    return new_output


if __name__ == '__main__':
    main()
