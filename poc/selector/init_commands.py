from functools import partial
from typing import Any

from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.commands.ChainCommand import ChainCommand
from selector.commands.ChangeLabelCommand import ChangeLabelCommand
from selector.commands.ChangeModeCommand import ChangeModeCommand
from selector.commands.CloseAppCommand import CloseAppCommand
from selector.commands.EndSelectingCommand import EndSelectingCommand
from selector.commands.ForceCloseAppCommand import ForceCloseAppCommand
from selector.commands.ForceSaveCommand import ForceSaveCommand
from selector.commands.GoToImageCommand import GoToImageCommand
from selector.commands.NextImageCommand import NextImageCommand
from selector.commands.NextLabelCommand import NextLabelCommand
from selector.commands.PrevImageCommand import PrevImageCommand
from selector.commands.PrevLabelCommand import PrevLabelCommand
from selector.commands.RemoveSelectedCommand import RemoveSelectedCommand
from selector.commands.StartSelectingCommand import StartSelectingCommand
from selector.commands.WheelLabelCommand import WheelLabelCommand
from selector.gui.components.ImageCanvas import ImageCanvas


def init_default_commands(app: Selector, model: SelectorModel) -> None:
    defaults_args = app, model

    # canvas = app.nametowidget("!mainwindow.image_canvas_container.!canvas")
    image_canvas: ImageCanvas = app.nametowidget("!mainwindow.!imagecanvas")

    app.add_mode("default")
    app.add_mode("selecting")

    register_partial = partial(
        register_command,
        app=app,
        target=app,
        mode_name="default",
        args=defaults_args,
        history_flag=True,
    )
    register_chain_partial = partial(
        register_chain_command,
        default_args=defaults_args,
        app=app,
        target=app,
        mode_name="default",
        history_flag=True,
    )

    # canvas
    # self.bind("<Configure>", lambda e: self.refresh_image())
    # self.bind("<Configure>", lambda e: self.refresh_image())

    # Arrows
    key = "<KeyRelease-Right>"
    command = NextImageCommand
    register_partial(key=key, command=command)

    key = "<Control-KeyRelease-Right>"
    command = GoToImageCommand
    args = defaults_args + (model.get_selector_data_len() - 1,)
    register_partial(key=key, command=command, args=args)

    key = "<KeyRelease-Left>"
    command = PrevImageCommand
    register_partial(key=key, command=command)

    key = "<Control-KeyRelease-Left>"
    command = GoToImageCommand
    args = defaults_args + (0,)
    register_partial(key=key, command=command, args=args)

    # WSAD - aka tryb gamingowy
    key = "<KeyRelease-w>"
    command = NextLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    key = "<KeyRelease-s>"
    command = PrevLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    key = "<KeyRelease-a>"
    command = PrevImageCommand
    register_partial(key=key, command=command)

    key = "<KeyRelease-d>"
    command = NextImageCommand
    register_partial(key=key, command=command)

    key = "<KeyRelease-space>"
    command = NextImageCommand
    register_partial(key=key, command=command)

    key = "<KeyRelease-Return>"
    commands = [[CloseAppCommand, defaults_args],
                [ForceSaveCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    # labels
    class_offset = 1
    for class_id in model.labels:
        key = str(class_id + class_offset)
        command = ChangeLabelCommand
        args = defaults_args + (class_id,)
        register_partial(key=key, command=command,
                         args=args, history_flag=False)

    # mouse
    key = "<Button-1>"  # left click
    commands = [[StartSelectingCommand, defaults_args + (image_canvas,)],
                [ChangeModeCommand, defaults_args + ("selecting",)]]
    register_chain_partial(key=key, commands=commands, target=image_canvas.canvas)

    key = "<Button-1>"
    mode = "selecting"
    commands = [[ChangeModeCommand, defaults_args + ("default",)],
                [EndSelectingCommand, defaults_args + (image_canvas,)]]
    register_chain_partial(key=key, commands=commands,
                           mode_name=mode, target=image_canvas.canvas)

    key = "<Button-3>"  # right click
    command = RemoveSelectedCommand
    args = defaults_args + (image_canvas,)
    register_partial(key=key, command=command, target=image_canvas.canvas, args=args)

    key = "<MouseWheel>"
    command = WheelLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    # global
    key = "<KeyRelease-Escape>"
    commands = [[ForceSaveCommand, defaults_args],
                [ForceCloseAppCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands, history_flag=False)

    commands = [[ForceSaveCommand, defaults_args],
                [ForceCloseAppCommand, defaults_args]]
    clicked_exit_partial = partial(clicked_exit, commands)
    app.protocol("WM_DELETE_WINDOW", clicked_exit_partial)

    app.bind("<Control-KeyPress-z>", lambda e: app.undo())

    app.activate_mode("default")


def clicked_exit(commands):
    for command_args in commands:
        command, args = command_args
        command(*args).execute()


def register_chain_command(commands: list[list[type, Any]], default_args: tuple, **kwargs):
    command = ChainCommand
    args = default_args + (commands,)

    register_command(command=command, args=args, **kwargs)


def register_command(app: Selector, target: Any, key: str, mode_name: str,
                     command: type, args: tuple, history_flag: bool):
    if history_flag:
        event = app.register_command_in_history(command, *args)
    else:
        event = app.register_command_without_history(command, *args)

    app.register_to_mode(mode_name, target, key, event)


def unbind_event(target: Any, event_key: str) -> None:
    target.unbind(event_key)
