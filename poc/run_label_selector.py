import glob
from pathlib import Path

import click
import yaml

from io_utils.utils import make_directories
from label_selector.LabelSelector import LabelSelector
from label_selector.init_commands import init_commands
from yolo.YoloDataset import YoloDataset


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="directory with images")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              help="output directory")
@click.option("-msc", "--label_selector_config", "label_selector_config",
              required=True, type=click.Path(exists=True), default="resources/run_label_selector.yaml",
              help="config")
@click.option("-ext", "--extension", "extension",
              required=True, type=str, default=".jpg",
              help="extension of images with dot")
def main(input_dir, output_dir, label_selector_config, extension):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    make_directories(output_dir, images_dir, labels_dir)

    with open(label_selector_config) as f:
        label_selector_config = yaml.load(f, Loader=yaml.FullLoader)

    glob_mask = "*" + extension
    images = glob.glob(str(input_dir / glob_mask))
    images = [Path(i) for i in images]

    app = LabelSelector(images, label_selector_config["names"])
    init_commands(app)
    app.load_checkpoint()
    app.mainloop()

    if app.to_export:
        dataset_parts = app.export_dataset_parts()
        yolo_dataset = YoloDataset(input_dir, output_dir,
                                   yolo_dataset_parts=dataset_parts,
                                   image_extension=extension)
        yolo_dataset.export()


if __name__ == '__main__':
    main()
