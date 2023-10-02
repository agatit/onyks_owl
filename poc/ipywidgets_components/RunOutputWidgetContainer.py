from IPython.core import display
from ipywidgets import Button, Output

from IPython.display import display


class RunOutputWidgetContainer:
    def __init__(self, title, button_callback, output_callback):
        self.title = title
        self.button = Button(description="Run")
        self.output_callback = output_callback

        self.output = Output()
        self.title_output = Output()
        self.widgets = []

        self.button.on_click(self.wrapp_on_click(button_callback))

    def wrapp_on_click(self, on_click):
        def wrapper(button):
            on_click(button)
            self.show_output()

        return wrapper

    def add_widgets(self, *widget):
        self.widgets.append(*widget)

    def show_output(self):
        self.output.clear_output()

        with self.output:
            self.output_callback()

    def render(self):
        display(self.title_output)
        display(*self.widgets)
        display(self.button, self.output)

        with self.title_output:
            print(self.title)

