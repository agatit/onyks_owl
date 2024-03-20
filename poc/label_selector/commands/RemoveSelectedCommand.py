import tkinter
from dataclasses import field
from functools import partial

from label_selector.commands.Command import Command
from yolo.YoloFormat import BoundingBox


class RemoveSelectedCommand(Command):
    removed_items: list = field(init=False, repr=False, default_factory=list)
    removed_data_index: int = field(init=False, repr=False)

    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app
        main_window = self.main_window
        current_index = app.current_index

        canvas_x, canvas_y = event.x, event.y
        image_x, image_y = main_window.resize_point_to_original(canvas_x, canvas_y)

        process_data = app.process_data[current_index]
        label_rectangles = process_data.label_rectangles

        image_xy = image_x, image_y
        condition = partial(self._point_in_bounds, image_xy)

        items_to_remove = [i for i in label_rectangles if condition(i.bounding_box)]

        if len(items_to_remove) > 0:
            self.removed_data_index = current_index
            self.removed_items = items_to_remove

            items_to_remove.sort(key=lambda x: self._bounding_box_area(x.bounding_box))
            process_data.label_rectangles.remove(items_to_remove[0])

            app.reload_image()
            return True

        else:
            return False

    def undo(self) -> None:
        label_rectangles = self.app.process_data[self.removed_data_index].label_rectangles
        for i in self.removed_items:
            label_rectangles.append(i)

        self.app.reload_image()

    @staticmethod
    def _point_in_bounds(point: tuple[int, int], bounding_box: BoundingBox) -> bool:
        x_condition = bounding_box.x1 <= point[0] <= bounding_box.x2
        y_condition = bounding_box.y1 <= point[1] <= bounding_box.y2

        return x_condition and y_condition

    @staticmethod
    def _bounding_box_area(bounding_box: BoundingBox) -> float:
        width = abs(bounding_box.x1 - bounding_box.x2)
        height = abs(bounding_box.y1 - bounding_box.y2)

        return width * height
