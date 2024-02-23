from functools import partial

from label_selector.LabelSelector import LabelSelector
from label_selector.commands.AcceptImageCommand import AcceptImageCommand
from label_selector.commands.ChainCommand import ChainCommand
from label_selector.commands.ChangeLabelCommand import ChangeLabelCommand
from label_selector.commands.ChangeModeCommand import ChangeModeCommand
from label_selector.commands.CloseAppCommand import CloseAppCommand
from label_selector.commands.EndSelectingCommand import EndSelectingCommand
from label_selector.commands.ForceCloseAppCommand import ForceCloseAppCommand
from label_selector.commands.NextImageCommand import NextImageCommand
from label_selector.commands.NextLabelCommand import NextLabelCommand
from label_selector.commands.PrevImageCommand import PrevImageCommand
from label_selector.commands.RejectImageCommand import RejectImageCommand
from label_selector.commands.RemoveSelectedCommand import RemoveSelectedCommand
from label_selector.commands.StartSelectingCommand import StartSelectingCommand
from label_selector.commands.WheelLabelCommand import WheelLabelCommand


def init_commands(app: LabelSelector) -> None:
    main_window = app.main_window

    defaults_args = app, main_window

    app.add_mode("default")
    app.add_mode("selecting")

    bind_event_partial = partial(
        register_command,
        app=app,
        target=app,
        mode_name="default",
        args=defaults_args,
        history_flag=True,
    )

    # keyboard
    key = "<Right>"
    command = NextImageCommand
    bind_event_partial(key=key, command=command)

    key = "<Left>"
    command = PrevImageCommand
    bind_event_partial(key=key, command=command)

    key = "<Tab>"
    command = NextLabelCommand
    bind_event_partial(key=key, command=command, history_flag=False)

    key = "<Control-KeyPress-s>"
    command = CloseAppCommand
    bind_event_partial(key=key, command=command)

    key = "<space>"
    commands = [[RejectImageCommand, defaults_args],
                [NextImageCommand, defaults_args]]
    command = ChainCommand
    args = defaults_args + (commands,)
    bind_event_partial(key=key, command=command, args=args)

    key = "<Return>"
    commands = [[AcceptImageCommand, defaults_args],
                [NextImageCommand, defaults_args]]
    command = ChainCommand
    args = defaults_args + (commands,)
    bind_event_partial(key=key, command=command, args=args)

    # labels
    for class_id, label in app.labels.items():
        command = ChangeLabelCommand
        key = str(class_id)
        args = defaults_args + (class_id, label)
        bind_event_partial(key=key, command=command,
                           args=args, history_flag=False)

    # mouse
    key = "<Button-1>"  # left click
    commands = [[StartSelectingCommand, defaults_args],
                [ChangeModeCommand, defaults_args + ("selecting",)]]
    command = ChainCommand
    args = defaults_args + (commands,)
    bind_event_partial(key=key, command=command,
                       args=args, target=app.main_window.image_canvas)

    key = "<Button-1>"
    mode = "selecting"
    commands = [[ChangeModeCommand, defaults_args + ("default",)],
                [EndSelectingCommand, defaults_args]]
    command = ChainCommand
    args = defaults_args + (commands,)
    bind_event_partial(key=key, command=command, mode_name=mode,
                       args=args, target=app.main_window.image_canvas)

    key = "<Button-3>"  # right click
    command = RemoveSelectedCommand
    bind_event_partial(key=key, command=command, target=app.main_window.image_canvas)

    key = "<MouseWheel>"
    command = WheelLabelCommand
    bind_event_partial(key=key, command=command, history_flag=False)

    # global
    key = "<Escape>"
    command = ForceCloseAppCommand
    bind_event_partial(key=key, command=command)

    app.bind("<Control-KeyPress-z>", lambda e: app.undo())

    app.activate_mode("default")


def register_command(app, target, key, mode_name, command, args, history_flag):
    if history_flag:
        event = app.register_command_in_history(command, *args)
    else:
        event = app.register_command_without_history(command, *args)

    app.modes[mode_name].register(target, key, event)
