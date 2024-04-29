import json
from pathlib import Path

import click
import yaml

from io_utils.utils import make_directories


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
    labels_dir = output_dir / "labels"
    make_directories(output_dir, images_dir, labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with open(input_dir / "output.json", "r") as file:
        output_json = json.load(file)


if __name__ == '__main__':
    main()

