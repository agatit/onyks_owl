import numpy as np
from ipywidgets import widgets


def filter_error(df):
    headers = ["frame", "x", "y"]
    df_velocity = df[headers]

    df_velocity_mean = df_velocity.groupby(
        "frame").transform("mean").add_prefix("mean_")
    df_velocity_std = df_velocity.groupby(
        "frame").transform("std").add_prefix("std_")

    df_velocity = df_velocity.join(df_velocity_mean)
    df_velocity = df_velocity.join(df_velocity_std)

    df_velocity = df_velocity.assign(
        diff_from_mean_x=lambda x: np.abs(x.x - x.mean_x))
    df_velocity = df_velocity.assign(
        diff_from_mean_y=lambda x: np.abs(x.y - x.mean_y))

    global_std_x = df_velocity_std["std_x"].std()
    global_std_y = df_velocity_std["std_y"].std()

    magnitude = {
        "global": 4,
        "local": 3
    }

    # global_condition = (df_velocity.diff_from_mean_x < global_std_x * magnitude["global"]) & (
    # df_velocity.diff_from_mean_y < global_std_y * magnitude["global"])
    local_condition = (df_velocity.diff_from_mean_x < df_velocity.std_x * magnitude["local"]) & (
            df_velocity.diff_from_mean_y < df_velocity.std_y * magnitude["local"])
    filtered_velocity = df_velocity[local_condition][headers]
    # filtered_velocity = df_velocity[local_condition &
    # global_condition][headers]
    return filtered_velocity


def df_frame_int_range_slider(df, step=10):
    min_frame = df["frame"].min()
    max_frame = df["frame"].max()
    int_range_slider_kwargs = {
        "value": [min_frame, max_frame],
        "min": min_frame,
        "max": max_frame,
        "step": step,
        "description": "Frame range: "
    }

    return widgets.IntRangeSlider(**int_range_slider_kwargs)


def iterate_over_df_with_window(df, callback, df_frame_range, window_size, window_step):
    first_frame, last_frame = df_frame_range
    last_frame += window_size

    left_iterator = range(first_frame, last_frame, window_step)
    right_iterator = range(window_size + first_frame, last_frame, window_step)

    for left_frame, right_frame in zip(left_iterator, right_iterator):
        condition = (df["frame"] >= left_frame) & \
                    (df["frame"] <= right_frame)
        df_part = df.loc[condition].reset_index()

        if not df_part.empty:
            callback(df_part)
