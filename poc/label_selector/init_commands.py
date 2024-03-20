from functools import partial
from typing import Any

from label_selector.LabelSelector import LabelSelector
from label_selector.commands.ChainCommand import ChainCommand
from label_selector.commands.ChangeLabelCommand import ChangeLabelCommand
from label_selector.commands.ChangeModeCommand import ChangeModeCommand
from label_selector.commands.CloseAppCommand import CloseAppCommand
from label_selector.commands.EndSelectingCommand import EndSelectingCommand
from label_selector.commands.ForceCloseAppCommand import ForceCloseAppCommand
from label_selector.commands.GoToImageCommand import GoToImageCommand
from label_selector.commands.NextImageCommand import NextImageCommand
from label_selector.commands.PrevImageCommand import PrevImageCommand
from label_selector.commands.RemoveSelectedCommand import RemoveSelectedCommand
from label_selector.commands.SaveCheckpointCommand import SaveCheckpointCommand
from label_selector.commands.StartSelectingCommand import StartSelectingCommand
from label_selector.commands.WheelLabelCommand import WheelLabelCommand


def init_default_commands(app: LabelSelector) -> None:
    main_window = app.main_window
    defaults_args = app, main_window

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

    # keyboard
    key = "<KeyRelease-Right>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [NextImageCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    key = "<Control-KeyRelease-Right>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [GoToImageCommand, defaults_args + (app.max_index - 1,)]]
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-Left>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [PrevImageCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    key = "<Control-KeyRelease-Left>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [GoToImageCommand, defaults_args + (0,)]]
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-space>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [NextImageCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-Return>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [CloseAppCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    # labels
    class_offset = 1
    for class_id, label in app.labels.items():
        key = str(class_id + class_offset)
        command = ChangeLabelCommand
        args = defaults_args + (class_id, label)
        register_partial(key=key, command=command,
                         args=args, history_flag=False)

    # mouse
    key = "<Button-1>"  # left click
    commands = [[StartSelectingCommand, defaults_args],
                [ChangeModeCommand, defaults_args + ("selecting",)]]
    register_chain_partial(key=key, commands=commands, target=app.main_window.image_canvas)

    key = "<Button-1>"
    mode = "selecting"
    commands = [[ChangeModeCommand, defaults_args + ("default",)],
                [EndSelectingCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands,
                           mode_name=mode, target=app.main_window.image_canvas)

    key = "<Button-3>"  # right click
    command = RemoveSelectedCommand
    register_partial(key=key, command=command, target=app.main_window.image_canvas)

    key = "<MouseWheel>"
    command = WheelLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    # global
    key = "<KeyRelease-Escape>"
    commands = [[SaveCheckpointCommand, defaults_args],
                [ForceCloseAppCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands, history_flag=False)

    app.protocol("WM_DELETE_WINDOW", lambda: ForceCloseAppCommand(*defaults_args).execute())
    app.bind("<Control-KeyPress-z>", lambda e: app.undo())

    app.activate_mode("default")


def register_command(app: LabelSelector, target: Any, key: str, mode_name: str,
                     command: type, args: tuple, history_flag: bool):
    if history_flag:
        event = app.register_command_in_history(command, *args)
    else:
        event = app.register_command_without_history(command, *args)

    app.register_to_mode(mode_name, target, key, event)


def register_chain_command(commands: list[list[type, Any]], default_args: tuple, **kwargs):
    command = ChainCommand
    args = default_args + (commands,)

    register_command(command=command, args=args, **kwargs)


def unbind_event(target: Any, event_key: str) -> None:
    target.unbind(event_key)
