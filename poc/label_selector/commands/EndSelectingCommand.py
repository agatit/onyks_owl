from dataclasses import dataclass

from label_selector.commands.Command import Command
from label_selector.gui.LabelRectangle import LabelRectangle
from yolo.YoloFormat import BoundingBox


@dataclass
class EndSelectingCommand(Command):
    canvas_x1y1_backup = None
    image_x1y1_backup = None

    def execute(self, event=None) -> bool:
        app = self.app
        main_window = self.main_window
        current_index = app.current_index

        start_point_image = app.start_point
        start_point_canvas = main_window.resize_point_to_canvas(
            start_point_image[0], start_point_image[1]
        )
        end_point_canvas = event.x, event.y
        end_point_image = main_window.resize_point_to_original(
            end_point_canvas[0], end_point_canvas[1]
        )

        canvas_x1y1, canvas_x2y2 = self.calculate_x1y1_x2y2(*start_point_canvas, *end_point_canvas)
        image_x1y1, image_x2y2 = self.calculate_x1y1_x2y2(*start_point_image, *end_point_image)

        self.canvas_x1y1_backup = canvas_x1y1
        self.image_x1y1_backup = image_x1y1

        # delete start point
        start_point_ref = app.process_data[current_index].start_point_ref
        main_window.image_canvas.delete(start_point_ref)

        # draw rectangle
        label_text = app.selected_label_text
        label_id = app.selected_label_id
        label = f"{label_id}_{label_text}"
        main_window.draw_label_rectangle(canvas_x1y1, canvas_x2y2, label)

        # save label_rectangle
        bounding_box = BoundingBox.from_x1y1_x2y2(image_x1y1, image_x2y2)
        label_rectangle = LabelRectangle(label_id, label_text, bounding_box)
        app.process_data[current_index].label_rectangles.append(label_rectangle)

        return True

    def undo(self) -> None:
        app = self.app
        main_window = self.main_window
        current_index = app.current_index

        image_x, image_y = self.image_x1y1_backup
        canvas_x, canvas_y = self.canvas_x1y1_backup

        # remove last rectangle
        app.process_data[current_index].label_rectangles.pop()
        self.app.reload_image()

        # draw star point
        app.start_point = (image_x, image_y)
        start_point_ref = main_window.draw_start_point(canvas_x, canvas_y)
        app.process_data[current_index].start_point_ref = start_point_ref

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

