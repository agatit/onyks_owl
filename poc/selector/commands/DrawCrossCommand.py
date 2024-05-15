import tkinter
from dataclasses import dataclass, field

from selector.commands.Command import Command
from selector.gui.components.ImageCanvas import ImageCanvas


@dataclass
class DrawCrossCommand(Command):
    image_canvas: ImageCanvas
    draw_callback_name: str

    _event: tkinter.Event = field(init=False, repr=False)

    def execute(self, event: tkinter.Event = None) -> bool:
        self._event = event
        self.image_canvas.draw_callbacks[self.draw_callback_name] = self._draw
        # self.app.notify_listener("reload_image")

        return True

    def undo(self) -> None:
        pass

    def _draw(self, canvas: tkinter.Canvas) -> None:
        x, y = self._event.x, self._event.y
        width, height = canvas.winfo_width(), canvas.winfo_height()

        horizontal_line = (0, y, width, y)
        vertical_line = (x, 0, x, height)

        canvas.create_line(*horizontal_line)
        canvas.create_line(*vertical_line)
