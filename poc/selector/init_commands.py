from functools import partial
from typing import Any, Protocol

from selector.Selector import Selector
from selector.commands.ChainCommand import ChainCommand
from selector.commands.ChangeLabelCommand import ChangeLabelCommand
from selector.commands.ChangeModeCommand import ChangeModeCommand
from selector.commands.CloseAppCommand import CloseAppCommand
from selector.commands.EndSelectingCommand import EndSelectingCommand
from selector.commands.ForceCloseAppCommand import ForceCloseAppCommand
from selector.commands.ForceSaveCommand import ForceSaveCommand
from selector.commands.GoToImageCommand import GoToImageCommand
from selector.commands.listbox.ChangeLabelToSelectedCommand import ChangeLabelToSelectedCommand
from selector.commands.listbox.GlowSelectedLabelCommand import GlowSelectedLabelCommand
from selector.commands.listbox.RemoveLabelCommand import RemoveLabelCommand
from selector.commands.listbox.SelectLabelCommand import SelectLabelCommand
from selector.commands.NextImageCommand import NextImageCommand
from selector.commands.NextLabelCommand import NextLabelCommand
from selector.commands.PrevImageCommand import PrevImageCommand
from selector.commands.PrevLabelCommand import PrevLabelCommand
from selector.commands.RemoveSelectedCommand import RemoveSelectedCommand
from selector.commands.StartSelectingCommand import StartSelectingCommand
from selector.commands.WheelLabelCommand import WheelLabelCommand


def init_default_commands(app: Selector) -> None:
    main_window = app.main_window
    defaults_args = app, main_window

    image_canvas = app.nametowidget("!mainwindow.!canvas")
    classes_listbox = app.nametowidget("!mainwindow.sidebar.class_listbox.listbox_container.!listbox")
    results_listbox = app.nametowidget("!mainwindow.sidebar.results_listbox.listbox_container.!listbox")
    remove_button = app.nametowidget("!mainwindow.sidebar.results_listbox.remove_button")
    change_button = app.nametowidget("!mainwindow.sidebar.results_listbox.change_button")

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

    # todo: do jakieś struktury
    go_to_next_image = [
        [NextImageCommand, defaults_args],
    ]

    go_to_last_image = [
        [GoToImageCommand, defaults_args + (app.max_index - 1,)],
    ]

    go_to_previous_image = [
        [PrevImageCommand, defaults_args],
    ]

    go_to_first_image = [
        [GoToImageCommand, defaults_args + (0,)],
    ]

    # Arrows
    key = "<KeyRelease-Right>"
    commands = go_to_next_image
    register_chain_partial(key=key, commands=commands)

    key = "<Control-KeyRelease-Right>"
    commands = go_to_last_image
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-Left>"
    commands = go_to_previous_image
    register_chain_partial(key=key, commands=commands)

    key = "<Control-KeyRelease-Left>"
    commands = go_to_first_image
    register_chain_partial(key=key, commands=commands)

    # WSAD - aka tryb gamingowy
    key = "<KeyRelease-w>"
    command = NextLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    key = "<KeyRelease-s>"
    command = PrevLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    key = "<KeyRelease-a>"
    commands = go_to_previous_image
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-d>"
    commands = go_to_next_image
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-space>"
    commands = go_to_next_image
    register_chain_partial(key=key, commands=commands)

    key = "<KeyRelease-Return>"
    commands = [[CloseAppCommand, defaults_args],
                [ForceSaveCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands)

    # labels
    class_offset = 1
    for class_id in app.labels:
        key = str(class_id + class_offset)
        command = ChangeLabelCommand
        args = defaults_args + (class_id,)
        register_partial(key=key, command=command,
                         args=args, history_flag=False)

    # mouse
    key = "<Button-1>"  # left click
    commands = [[StartSelectingCommand, defaults_args],
                [ChangeModeCommand, defaults_args + ("selecting",)]]
    register_chain_partial(key=key, commands=commands, target=image_canvas)

    key = "<Button-1>"
    mode = "selecting"
    commands = [[ChangeModeCommand, defaults_args + ("default",)],
                [EndSelectingCommand, defaults_args]]
    register_chain_partial(key=key, commands=commands,
                           mode_name=mode, target=image_canvas)

    key = "<Button-3>"  # right click
    command = RemoveSelectedCommand
    register_partial(key=key, command=command, target=image_canvas)

    key = "<MouseWheel>"
    command = WheelLabelCommand
    register_partial(key=key, command=command, history_flag=False)

    # key = "<Motion>"
    # command = DrawCrossCommand
    # register_partial(key=key, command=command, history_flag=False,
    #                  target=image_canvas)
    #
    # key = "<Motion>"
    # command = DrawCrossCommand
    # register_partial(key=key, command=command, mode_name="selecting", history_flag=False,
    #                  target=image_canvas)

    # list boxes
    key = "<<ListboxSelect>>"
    command = SelectLabelCommand
    args = defaults_args + (classes_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=False,
                     target=classes_listbox)

    key = "<<ListboxSelect>>"
    command = GlowSelectedLabelCommand
    args = defaults_args + (results_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=False,
                     target=results_listbox)

    key = "<KeyRelease-Delete>"
    command = RemoveLabelCommand
    args = defaults_args + (results_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=True,
                     target=results_listbox)

    key = "<Button-1>"
    command = RemoveLabelCommand
    args = defaults_args + (results_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=True,
                     target=remove_button)

    key = "<Button-1>"
    command = ChangeLabelToSelectedCommand
    args = defaults_args + (results_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=True,
                     target=change_button)

    key = "<KeyRelease-Return>"
    command = ChangeLabelToSelectedCommand
    args = defaults_args + (results_listbox,)
    register_partial(key=key, command=command, args=args, history_flag=True,
                     target=results_listbox)

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
