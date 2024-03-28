import json
import os
import sys
from pathlib import Path

import click
import yaml
from PIL import Image

from find_frames_with_tags_scripts.output_utils import init_datasets_from_output_json
from io_utils.utils import make_directories
from label_selector.LabelSelector import LabelSelector
from label_selector.gui.LabelRectangle import LabelRectangle
from label_selector.gui.utils import open_loading_screen
from label_selector.init_commands import init_default_commands
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
def main(input_dir, output_dir, config, quick_export):
    # pickle dump recursion error
    sys.setrecursionlimit(10000)

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

    image_extension = config["image_extension"]
    yolo_datasets = init_datasets_from_output_json(input_dir, output_dir, output_json, image_extension)

    labels = config["names"]
    max_image_number = config["max_images"]
    for dataset in yolo_datasets:
        app = SelectFramesWithTags(dataset, labels, max_image_number)
        init_default_commands(app)

        try:
            app.load_checkpoint()
        except FileNotFoundError:
            print(f"Not found: {app.checkpoint_name}")

        if quick_export > 0:
            app.destroy()

            new_parts = app.export_dataset_parts()[:quick_export]
            dataset.yolo_dataset_parts = new_parts
            dataset.export()
            continue

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


class SelectFramesWithTags(LabelSelector):
    def __init__(self, dataset: YoloDataset, labels: dict[int, str], max_images: int = -1):
        images = [i.original_image_path for i in dataset.yolo_dataset_parts]
        checkpoint_name = '.' + dataset.dataset_name

        super().__init__(images, labels, checkpoint_name, max_images)
        self._load_yolo_dataset_parts(dataset, labels)

        self.reload_main_window()
        self.deiconify()

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

    def load_checkpoint(self) -> None:
        last_checkpoint = self._select_latest_checkpoint()
        checkpoint = self._load_from_pickle(last_checkpoint)

        self.current_index = checkpoint.current_index
        self.process_data = checkpoint.process_data

        self.reload_main_window()
        self.max_index = len(self.process_data)


if __name__ == '__main__':
    main()
