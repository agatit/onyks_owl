import os.path
import shutil
from itertools import tee, accumulate
from pathlib import Path

import click
import numpy as np
import yaml

from io_utils.utils import make_directories, make_clean_dir


@click.command()
@click.option("-i", "--image_dir", "input_image_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="directory with images")
@click.option("-l", "--label_dir", "input_label_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="directory with labels in Darknet txt format")
@click.option("-out", "--output_dir", "output_dir",
              required=True, type=click.Path(),
              help="output directory for yolo dataset")
@click.option("-c", "--config", "config",
              required=True, type=click.Path(exists=True),
              default="resources/make_yolo_dataset.yaml",
              help="make_yolo_dataset.yaml file")
def main(input_image_dir, input_label_dir, output_dir, config):
    with open(config) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    input_image_dir = Path(input_image_dir)
    input_label_dir = Path(input_label_dir)
    output_dir = Path(output_dir)

    make_clean_dir(output_dir)

    images_paths = [i for i in input_image_dir.iterdir() if i.is_file()]
    labels_paths = [i for i in input_label_dir.iterdir() if i.is_file()]
    # assert len(images_paths) == len(labels_paths), "Number of images and labels is not equal"

    sets_names = config["split_ratio"].keys()
    output_images_paths = init_output_dirs(output_dir, "images", sets_names)
    output_labels_paths = init_output_dirs(output_dir, "labels", sets_names)

    split_dataset = split_list_by_percentage(images_paths, config["split_ratio"].values())
    split_dataset = {name: data for name, data in zip(sets_names, split_dataset)}

    for set_name in sets_names:
        image_dataset = split_dataset[set_name]
        files_name = [i.stem for i in image_dataset]
        label_dataset = [i for i in labels_paths if i.stem in files_name]

        for image_path in image_dataset:
            copy_image_to_dataset(image_path, output_images_paths[set_name])

        for label_path in label_dataset:
            copy_image_to_dataset(label_path, output_labels_paths[set_name])

    dataset_yaml = init_dataset_yaml(config, output_images_paths)
    dataset_yaml_path = output_dir / "dataset.yaml"

    with open(dataset_yaml_path, "w") as file:
        yaml.dump(dataset_yaml, file)


def init_dataset_yaml(config: dict, datasets_paths: dict[str, Path]) -> dict:
    dataset_yaml = {"names": config["names"].copy()}
    # dataset_yaml["nc"] = len(dataset_yaml["names"])

    for dataset_name, path in datasets_paths.items():
        dataset_yaml[dataset_name] = os.path.abspath(path)

    dataset_yaml["training"] = config["training"].copy()
    dataset_yaml["augmentation"] = config["augmentation"].copy()

    return dataset_yaml


def copy_image_to_dataset(image_path: Path, current_dataset_path: Path) -> None:
    full_name = image_path.name
    output_path = current_dataset_path / full_name
    shutil.copyfile(image_path, output_path)


def init_output_dirs(output_dir: Path, sub_dir_name: str, sub_sub_dir_names: list[str]) -> dict[str, Path]:
    sub_dir_path = output_dir / sub_dir_name
    make_directories(sub_dir_path)

    sub_sub_dir_paths = {name: sub_dir_path / name for name in sub_sub_dir_names}
    make_directories(*sub_sub_dir_paths.values())

    return sub_sub_dir_paths


def split_list_by_percentage(_list: list, percentage: list[int]) -> list[np.ndarray]:
    split_numbers = split_number(len(_list), *percentage)
    indexes = list(accumulate(split_numbers))

    return np.split(_list, indexes)


def split_number(number: int, *percentage: int) -> list:
    result = [number * percent // 100 for percent in percentage]

    test_sum = sum(result)
    if test_sum != number:
        diff = number - test_sum
        result[0] += diff

    return result


if __name__ == '__main__':
    main()
