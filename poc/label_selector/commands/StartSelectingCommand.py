import tkinter

from label_selector.commands.Command import Command


class StartSelectingCommand(Command):

    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app
        main_window = self.main_window
        current_index = app.current_index

        canvas_x, canvas_y = event.x, event.y
        image_x, image_y = main_window.resize_point_to_original(canvas_x, canvas_y)

        # draw start point
        app.start_point = (image_x, image_y)
        start_point_ref = main_window.draw_start_point(canvas_x, canvas_y)
        app.process_data[current_index].start_point_ref = start_point_ref

        return True

    def undo(self) -> None:
        app = self.app
        main_window = self.main_window
        current_index = app.current_index

        # remove start point
        start_point_ref = app.process_data[current_index].start_point_ref
        if start_point_ref:
            main_window.image_canvas.delete(start_point_ref)
            app.process_data[current_index].start_point_ref = None

