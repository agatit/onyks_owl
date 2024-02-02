import json
from itertools import groupby
from pathlib import Path

import click
import yaml

from select_frames_with_tags_scripts.filter_output_json import filter_output_json
from yolo.DetectionResult import YoloFormat
from yolo.YoloDataset import YoloDataset
from yolo.YoloDatasetPart import YoloDatasetPart


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="find_with_frames_tags.py output directory")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              help="output directory")
@click.option("-fc", "--filter-config", "filter_config",
              type=click.Path(exists=True), default="resources/select_frames_with_tags.yaml",
              help="skip frame step")
@click.option("-a", "--auto", "auto_mode",
              is_flag=True,
              help="skip frame step")
def main(input_dir, output_dir, filter_config, auto_mode):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    make_output_dirs(output_dir)

    with open(input_dir / "output.json", "r") as file:
        output_json = json.load(file)

    if filter_config:
        with open(filter_config) as f:
            filter_config = yaml.load(f, Loader=yaml.FullLoader)

        filter_output_json(output_json, filter_config)

    yolo_datasets = init_datasets_from_output_json(input_dir, output_dir, output_json)

    if not auto_mode:
        # app = App(input_dir, output_dir)
        # app.mainloop()
        pass

    for dataset in yolo_datasets:
        dataset.export()


def init_datasets_from_output_json(input_dir, output_dir, output_json):
    yolo_datasets = []
    for dataset_name, frames in output_json.items():
        dataset_path = input_dir / dataset_name
        image_extension = Path(frames[0]["file_name"]).suffix

        yolo_dataset = YoloDataset(dataset_path, output_dir, image_extension)

        for frame_number, grouped_frames in groupby(frames, lambda frame: frame["frame_number"]):
            yolo_formats = [YoloFormat(**i["detection_result"]["yolo_format"]) for i in grouped_frames]

            image_name = str(frame_number) + image_extension
            image_path = dataset_path / image_name

            new_dataset_part = YoloDatasetPart(yolo_formats, image_path)
            yolo_dataset.yolo_dataset_parts.append(new_dataset_part)

        yolo_datasets.append(yolo_dataset)
    return yolo_datasets


def make_output_dirs(output_dir: Path):
    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"

    dirs = [output_dir, images_dir, labels_dir]
    for directory in dirs:
        if not directory.exists():
            directory.mkdir()

    return images_dir, labels_dir


if __name__ == '__main__':
    main()
