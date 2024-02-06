import glob
from datetime import datetime
from pathlib import Path


def get_current_time(time_format: str = "%Y%m%dT%H%M%S"):
    return datetime.now().strftime(time_format)


def timestamp_output_file(extension: str, timestamp: str, prefixes: list = None, suffixes: list = None,
                          concat_char: str = '_'):
    result = timestamp
    # if prefixes:

    return result + '.' + extension


def get_latest_file_from_directory(dir_path, extension):
    mask = dir_path + '*' + extension
    return max(glob.glob(mask))


def make_directories(*paths: Path) -> None:
    for directory in paths:
        if not directory.exists():
            directory.mkdir()
