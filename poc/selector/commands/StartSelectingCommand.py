import tkinter
from dataclasses import dataclass
from functools import partial

from selector.canvas_callbacks.draw.DrawStartingPoint import draw_starting_point
from selector.commands.Command import Command
from selector.gui.components.ImageCanvas import ImageCanvas


@dataclass
class StartSelectingCommand(Command):
    image_canvas: ImageCanvas

    # todo: na zewnątrz
    draw_starting_point_str = "draw_starting_point"

    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app
        image_canvas = self.image_canvas

        canvas_x, canvas_y = event.x, event.y
        image_x, image_y = image_canvas.resize_point_to_original(canvas_x, canvas_y)

        # draw start point
        app.start_drawing_point = (image_x, image_y)
        image_canvas.draw_callbacks[self.draw_starting_point_str] = partial(
            draw_starting_point,
            x=canvas_x,
            y=canvas_y
        )

        app.notify_listener("reload_image")

        return True

    def undo(self) -> None:
        app = self.app
        image_canvas = self.image_canvas

        # remove start point
        if self.draw_starting_point_str in image_canvas.draw_callbacks:
            del image_canvas.draw_callbacks[self.draw_starting_point_str]

        app.notify_listener("reload_image")
        app.notify_listener("reload_results_listbox")
