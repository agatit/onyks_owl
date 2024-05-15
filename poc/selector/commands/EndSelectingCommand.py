import tkinter
from dataclasses import dataclass, field
from functools import partial

from selector.canvas_callbacks.draw.DrawStartingPoint import draw_starting_point
from selector.commands.Command import Command
from selector.gui.LabelRectangle import LabelRectangle
from selector.gui.components.ImageCanvas import ImageCanvas
from yolo.YoloFormat import BoundingBox


@dataclass
class EndSelectingCommand(Command):
    image_canvas: ImageCanvas

    canvas_x1y1_backup = None
    image_x1y1_backup = None

    # todo: na zewnątrz
    draw_starting_point_str = "draw_starting_point"

    _label_rectangle_backup: LabelRectangle = field(init=False, default=None)

    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app
        image_canvas = self.image_canvas
        model = self.model

        # mapping
        start_point_image = app.start_drawing_point
        start_point_canvas = image_canvas.resize_point_to_canvas(
            start_point_image[0], start_point_image[1]
        )
        end_point_canvas = event.x, event.y
        end_point_image = image_canvas.resize_point_to_original(
            end_point_canvas[0], end_point_canvas[1]
        )

        canvas_x1y1, canvas_x2y2 = self.calculate_x1y1_x2y2(*start_point_canvas, *end_point_canvas)
        image_x1y1, image_x2y2 = self.calculate_x1y1_x2y2(*start_point_image, *end_point_image)

        self.canvas_x1y1_backup = canvas_x1y1
        self.image_x1y1_backup = image_x1y1

        # delete start point
        if self.draw_starting_point_str in image_canvas.draw_callbacks:
            del image_canvas.draw_callbacks[self.draw_starting_point_str]

        # save label_rectangle
        label_text = app.current_label_text
        label_id = app.current_label_id_var.get()
        bounding_box = BoundingBox.from_x1y1_x2y2(image_x1y1, image_x2y2)
        label_rectangle = LabelRectangle(label_id, label_text, bounding_box)

        self._label_rectangle_backup = label_rectangle

        current_data = model.get_selector_data(app.current_index_var.get())
        current_data.label_rectangles.append(label_rectangle)

        app.notify_listener("reload_image")
        app.notify_listener("reload_results_listbox")

        return True

    def undo(self) -> None:
        app = self.app
        image_canvas = self.image_canvas

        image_x, image_y = self.image_x1y1_backup
        canvas_x, canvas_y = self.canvas_x1y1_backup

        # remove last rectangle
        current_data = self.model.get_selector_data(self.app.current_index_var.get())
        label_rectangles = current_data.label_rectangles

        if self._label_rectangle_backup in label_rectangles:
            label_rectangle_index = label_rectangles.index(self._label_rectangle_backup)
            del label_rectangles[label_rectangle_index]

        # draw star point
        app.start_drawing_point = (image_x, image_y)
        image_canvas.draw_callbacks[self.draw_starting_point_str] = partial(
            draw_starting_point,
            x=canvas_x,
            y=canvas_y
        )

        app.notify_listener("reload_image")
        app.notify_listener("reload_results_listbox")

    @staticmethod
    def calculate_x1y1_x2y2(start_x, start_y, end_x, end_y) -> tuple:
        # first quarter
        if start_x <= end_x and start_y >= end_y:
            return (start_x, end_y), (end_x, start_y)
        # second
        elif start_x >= end_x and start_y >= end_y:
            return (end_x, end_y), (start_x, start_y)
        # third
        elif start_x >= end_x and start_y <= end_y:
            return (end_x, start_y), (start_x, end_y)
        # forth
        elif start_x <= end_x and start_y <= end_y:
            return (start_x, start_y), (end_x, end_y)
