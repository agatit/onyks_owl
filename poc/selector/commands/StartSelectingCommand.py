import tkinter

from selector.commands.Command import Command


class StartSelectingCommand(Command):

    def execute(self, event: tkinter.Event = None) -> bool:
        app = self.app
        main_window = self.app.main_window
        model = self.model
        current_index = app.current_index_var.get()

        canvas_x, canvas_y = event.x, event.y
        image_x, image_y = main_window.resize_point_to_original(canvas_x, canvas_y)

        # draw start point
        app.start_drawing_point = (image_x, image_y)
        start_point_ref = main_window.draw_start_point(canvas_x, canvas_y)
        current_data = model.get_selector_data(app.current_index_var.get())
        current_data.start_drawing_point_ref = start_point_ref

        return True

    def undo(self) -> None:
        app = self.app
        main_window = self.app.main_window
        model = self.model
        current_index = app.current_index_var.get()

        # remove start point
        current_data = model.get_selector_data(app.current_index_var.get())
        start_point_ref = current_data.start_drawing_point_ref
        if start_point_ref:
            main_window.image_canvas.delete(start_point_ref)
            current_data.start_drawing_point_ref = None

        app.notify_listener("reload_results_listbox")
