import os
from pathlib import Path
from typing import Iterable, Iterator

import click
import yaml

from find_frames_with_tags_scripts.output_json import load_output_json
from io_utils.utils import make_directories
from ocr.datasets.FullDatasetPart import FullDatasetPart
from selector.Selector import Selector
from selector.init_commands import init_default_commands
from selector.init_listeners import init_default_listeners
from selector.init_main_window import init_default_main_window


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default=".", help="find_with_frames_tags.py output directory")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              default=".", help="output directory")
@click.option("-c", "--config", "config",
              required=True, type=click.Path(exists=True),
              default="select_frames_with_tags.yaml", help="path to config")
def main(input_dir, output_dir, config):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    images_dir = output_dir / "images"
    make_directories(output_dir, images_dir)

    labels_json_path = output_dir / "labels.json"

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    output_json = load_output_json(input_dir)
    output_json = filter_output_json(output_json, config, input_dir)


def filter_output_json(output_json: dict, config: dict, input_dir: Path):
    dirs = os.listdir(input_dir)
    output_json = {k: v for k, v in output_json.items() if k in dirs}

    selected_labels = config["names"].keys()

    for dataset_name, results in output_json.items():
        selected_results = []

        for result in results:
            detection_result = result["detection_result"]

            if detection_result is not None and check_detection_result_id(detection_result, selected_labels):
                selected_results.append(result)

        output_json[dataset_name] = selected_results

    return output_json


def check_detection_result_id(detection_result: dict, enabled_id: Iterable) -> bool:
    return detection_result["yolo_format"]["class_id"] in enabled_id


class SelectNumbersData(FullDatasetPart):
    track_id: int
    proposed_text: str


def select_numbers_data_gen(output_json: dict) -> Iterator[SelectNumbersData]:
    pass


class SelectNumbers(Selector):
    def __init__(self, data: SelectNumbersData, *args, **kwargs):
        # images = [i.original_image_path for i in dataset.yolo_dataset_parts]
        # super().__init__(images, labels, save_manager, max_images, dataset.dataset_name, *args, **kwargs)
        pass

    def _init_main_window(self):
        init_default_main_window(self)

    def _init_commands(self):
        init_default_commands(self)

    def _init_listeners(self):
        init_default_listeners(self)


if __name__ == '__main__':
    main()
