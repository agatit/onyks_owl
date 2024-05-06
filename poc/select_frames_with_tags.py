import json
import os
import sys
import tkinter as tk
from pathlib import Path

import click
import yaml
from PIL import Image

from find_frames_with_tags_scripts.output_json import load_output_json
from find_frames_with_tags_scripts.output_utils import init_datasets_from_output_json
from io_utils.utils import make_directories
from io_utils.yaml import Options, init_options
from selector.gui.MainWindow import MainWindow
from selector.gui.components.ScaleWithLabel import ScaleWithLabel
from selector.gui.components.ScrollableListbox import ScrollableListbox
from selector.gui.components.TopBar import TopBar
from selector.init_listeners import init_default_listeners
from selector.init_main_window import init_default_main_window
from selector.saving.Checkpoint import Checkpoint, init_checkpoint
from selector.Selector import Selector
from selector.gui.LabelRectangle import LabelRectangle
from selector.gui.utils import open_loading_screen
from selector.init_commands import init_default_commands
from selector.saving.SaveManager import SaveManager
from yolo.YoloDataset import YoloDataset


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
@click.option("-qe", "--quick_export", "quick_export",
              type=int, default=-1,
              help="quick export mode, select number images to export")
@click.option("-li", "--last_image", "last_image",
              is_flag=True,
              help="last image mode, select number images to export")
def main(input_dir, output_dir, config, quick_export, last_image):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    make_directories(output_dir, images_dir, labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    output_json = load_output_json(input_dir)

    checkpoints: Options = {
        "auto1": init_checkpoint,
        "auto2": init_checkpoint
    }
    checkpoints = init_options(checkpoints, config["checkpoints"])

    dirs = os.listdir(input_dir)
    output_json = {k: v for k, v in output_json.items() if k in dirs}

    image_extension = config["image_extension"]
    yolo_datasets = init_datasets_from_output_json(input_dir, output_dir, output_json, image_extension)

    labels = config["names"]
    max_image_number = config["max_images"]

    for dataset in yolo_datasets:
        save_manager = SaveManager(dataset.dataset_name)
        [save_manager.add_checkpoint(checkpoint) for checkpoint in checkpoints]

        app = SelectFramesWithTags(dataset, labels, save_manager, max_image_number)

        try:
            app.load_checkpoint()
        except FileNotFoundError:
            print(f"Not found: {app.save_manager.get_latest_checkpoint()}")

        if app.to_export:
            app.destroy()
            continue

        app.mainloop()

        if not app.to_export:
            break

        new_parts = app.export_dataset_parts()
        dataset.yolo_dataset_parts = new_parts
        dataset.export()

        del app


class SelectFramesWithTags(Selector):
    def __init__(self, dataset: YoloDataset, labels: dict[int, str], save_manager: SaveManager, max_images: int = -1,
                 *args, **kwargs):
        images = [i.original_image_path for i in dataset.yolo_dataset_parts]
        super().__init__(images, labels, save_manager, max_images, dataset.dataset_name, *args, **kwargs)

        self._load_yolo_dataset_parts(dataset, labels)
        # self.notify_listener("reload_main_window")

    def _init_main_window(self):
        init_default_main_window(self)

    def _init_commands(self):
        init_default_commands(self)

    def _init_listeners(self):
        init_default_listeners(self)

    @open_loading_screen
    def _load_yolo_dataset_parts(self, dataset, labels):
        max_images = self.max_index

        for process_data, dataset_part, in zip(self.process_data[:max_images], dataset.yolo_dataset_parts[:max_images]):
            formats = dataset_part.yolo_formats

            label_rectangles = []
            for _format in formats:
                width, height = Image.open(dataset_part.original_image_path).size

                bounding_box = _format.to_bounding_box(width, height)

                label_rectangle = LabelRectangle(
                    label_id=_format.class_id,
                    label_text=labels[_format.class_id],
                    bounding_box=bounding_box
                )
                label_rectangles.append(label_rectangle)

            process_data.label_rectangles = label_rectangles


if __name__ == '__main__':
    main()
