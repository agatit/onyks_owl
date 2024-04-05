import logging
from itertools import product
from pathlib import Path

import click
import yaml
from tqdm import tqdm

from io_utils.utils import load_paths_with_extension
from yolo.YoloFormat import YoloFormat
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8


@click.command()
@click.option("-i", "--images", "images_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default="images", help="find_with_frames_tags.py output directory")
@click.option("-l", "--labels", "labels_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default="labels", help="output directory")
@click.option("-c", "--config", "config",
              required=True, type=click.Path(exists=True),
              default="filter_yolo_dataset.yaml.yaml", help="path to config")
@click.option("-m", "--model", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, help="yolo model path")
@click.option("-v", "--verbose", "verbose", is_flag=True,
              help="verbose mode")
def main(images_dir, labels_dir, config, model_path, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)

    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    image_extension = config["image"]["extension"]
    images = load_paths_with_extension(images_dir, image_extension)
    formats_labels_images = load_paths_with_extension(labels_dir, ".txt")

    detector = YoloDetectorV8(model_path, **config["model"])
    images_labels_paths = {i: l for i, l in product(images, formats_labels_images) if i.stem == l.stem}

    batch_size = detector.batch_size

    batch = []
    formats_labels_images = []
    max_index = len(images_labels_paths) - 1
    with tqdm(total=max_index) as pbar:
        for index, (image_path, label_path) in enumerate(images_labels_paths.items()):

            if len(batch) < batch_size:
                batch.append(image_path)

                formats_label_image = _yolo_formats_from_file(label_path), label_path, image_path
                formats_labels_images.append(formats_label_image)

                pbar.update()
                if index < max_index:
                    continue

            results = detector(batch)

            for frame_results, frame_formats_label_image in zip(results, formats_labels_images):
                frame_formats, frame_label_path, frame_image_path = frame_formats_label_image

                found_yolo_formats = _find_yolo_formats(frame_formats, frame_results)

                if len(found_yolo_formats) < 1:
                    frame_label_path.unlink()
                    frame_image_path.unlink()
                    logging.info(f"Deleted: {frame_label_path.stem}")
                    continue

                str_yolo_formats = [i.to_yolo_txt_line() for i in found_yolo_formats]

                with open(frame_label_path, "w") as file:
                    file.writelines(str_yolo_formats)

                logging.info(f"Updated: {frame_label_path.stem}")

            batch = []
            formats_labels_images = []


def _find_yolo_formats(frame_formats: list[YoloFormat], frame_results: list[YoloFormat]) -> list[YoloFormat]:
    formats = []

    for result, _format in product(frame_results, frame_formats):
        if result.yolo_format == _format:
            formats.append(_format)
            continue

    return formats


def _yolo_formats_from_file(label_path: Path) -> list[YoloFormat]:
    with open(label_path, "r") as file:
        return YoloFormat.load_from_file(file)


if __name__ == '__main__':
    main()
