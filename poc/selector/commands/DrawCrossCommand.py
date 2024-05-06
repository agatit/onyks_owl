import tkinter
from dataclasses import dataclass, field

from selector.commands.Command import Command


@dataclass
class DrawCrossCommand(Command):
    draw_callback_name: str = "cross"

    _mouse_event: tkinter.Event = field(init=False, repr=False)

    def execute(self, event: tkinter.Event = None) -> bool:
        self._mouse_event = event
        self.main_window.draw_callbacks[self.draw_callback_name] = self._draw

        self.app.notify_listener("reload_image")

        return True

    def undo(self) -> None:
        pass

    def _draw(self, canvas: tkinter.Canvas):
        x, y = self._mouse_event.x, self._mouse_event.y
        width, height = canvas.winfo_width(), canvas.winfo_height()

        horizontal_line = (0, y, width, y)
        vertical_line = (x, 0, x, height)

        canvas.create_line(*horizontal_line)
        canvas.create_line(*vertical_line)
