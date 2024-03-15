import json
import os
import sys
from pathlib import Path

import click
import yaml

from io_utils.utils import make_directories
from label_selector.LabelSelector import LabelSelector
from label_selector.init_commands import init_commands
from find_frames_with_tags_scripts.output_utils import init_datasets_from_output_json

# pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    config_path = Path(sys._MEIPASS) / "select_frames_with_tags.yaml"
else:
    config_path = "resources/select_frames_with_tags.yaml"


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default=".", help="find_with_frames_tags.py output directory")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              default=".", help="output directory")
@click.option("-c", "--config", "config",
              required=True, type=click.Path(exists=True), default=config_path,
              help="path to config")
@click.option("-ex", "--extension", "image_extension",
              type=str, default=".jpg",
              help="extension of images with dot")
def main(input_dir, output_dir, config, image_extension):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    make_directories(output_dir, images_dir, labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with open(input_dir / "output.json", "r") as file:
        output_json = json.load(file)

    dirs = os.listdir(input_dir)
    output_json = {k: v for k, v in output_json.items() if k in dirs}

    yolo_datasets = init_datasets_from_output_json(input_dir, output_dir, output_json, image_extension)

    labels = config["names"]
    max_image_number = int(config["max_images_number"])

    for dataset in yolo_datasets:
        app = LabelSelector.from_yolo_dataset(dataset, labels, max_image_number)
        init_commands(app)

        try:
            app.load_checkpoint()
        except Exception as e:
            print(f"Not found: {app.checkpoint_name}")

        current_index = app.current_index
        next_index = current_index + 1

        # check if dataset is complete
        if next_index == app.max_index:
            app.destroy()
            continue

        app.mainloop()

        if not app.to_export:
            break

        new_parts = app.export_dataset_parts()
        dataset.yolo_dataset_parts = new_parts
        dataset.export()


if __name__ == '__main__':
    main()
