from functools import partial
from typing import Any

from find_frames_with_tags_scripts.exporters import export_original_image, export_cropped_class, \
    export_bounding_box_image
from find_frames_with_tags_scripts.filtering.batch_filtering import init_efficientnet
from find_frames_with_tags_scripts.filtering.detecions_filtering import any_below_threshold_filter


def load_efficientnet(**kwargs) -> Any:
    return init_efficientnet()


def load_any_below_threshold(value: float = 0.7, **kwargs) -> Any:
    return partial(any_below_threshold_filter, upper_threshold=value)


def load_exporter_original_image(**kwargs) -> Any:
    return export_original_image


def load_exporter_cropped(classes: list[int] = None, **kwargs) -> Any:
    return partial(export_cropped_class, classes=classes)


def load_exporter_bounding_box_image(classes: list[int] = None, **kwargs) -> Any:
    return partial(export_bounding_box_image, classes=classes)
