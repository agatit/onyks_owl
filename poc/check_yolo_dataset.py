import sys
from itertools import product
from pathlib import Path

import click
import yaml
from PIL import Image

from io_utils.utils import load_paths_with_extension
from label_selector.LabelSelector import LabelSelector
from label_selector.gui.LabelRectangle import LabelRectangle
from label_selector.gui.utils import open_loading_screen
from label_selector.init_commands import init_default_commands
from yolo.YoloFormat import YoloFormat


@click.command()
@click.option("-i", "--images", "images_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default="images", help="find_with_frames_tags.py output directory")
@click.option("-lb", "--labels", "labels_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default="labels", help="output directory")
@click.option("-lc", "--labels_config", "config",
              required=True, type=click.Path(exists=True),
              default="check_yolo_dataset.yaml", help="path to config")
def main(images_dir, labels_dir, config):
    # pickle dump recursion error
    sys.setrecursionlimit(10000)

    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        labels_config = config["names"]

    image_extension = config["image_extension"]
    images = load_paths_with_extension(images_dir, image_extension)
    labels = load_paths_with_extension(labels_dir, ".txt")

    images_labels = [(i, l) for i, l in product(images, labels) if i.stem == l.stem]

    app = CheckYoloDataset(images_labels, labels_config)
    init_default_commands(app)

    # app.mainloop()
    # app.export()

    try:
        app.load_checkpoint()
    except FileNotFoundError as e:
        print(f"Not found: {app.save_manager.get_latest_checkpoint()}")

    app.mainloop()

    if app.to_export:
        app.export()


class CheckYoloDataset(LabelSelector):

    def __init__(self, images_labels: list[tuple[Path, Path]], labels: dict[int, str]):
        self.images_labels = dict(images_labels)

        images = list(self.images_labels.keys())
        super().__init__(images, labels)

        self.init_process_data()

    @open_loading_screen
    def init_process_data(self):
        labels = self.labels

        for image_path, label_path in self.images_labels.items():
            with open(label_path, "r") as file:
                lines = file.readlines()

            width, height = Image.open(image_path).size

            yolo_formats = [YoloFormat.from_yolo_txt(line) for line in lines]

            label_rectangles = []
            for yolo_format in yolo_formats:
                label_id = yolo_format.class_id
                label_text = labels[label_id]
                bounding_box = yolo_format.to_bounding_box(width, height)

                label_rectangle = LabelRectangle(label_id, label_text, bounding_box)
                label_rectangles.append(label_rectangle)

            process_data = [i for i in self.process_data if i.image_path == image_path][0]
            process_data.label_rectangles = label_rectangles

        self.notify_listener("reload_main_window")

    @open_loading_screen
    def export(self):
        for data in self.process_data:
            image_file = data.image_path
            label_file = self.images_labels[image_file]

            if len(data.label_rectangles) < 1:
                print("removed:", data.image_path.stem)
                image_file.unlink()
                label_file.unlink()
                continue

            yolo_formats = self._process_data_to_yolo_formats(data)

            str_yolo_formats = [i.to_yolo_txt_line() for i in yolo_formats]

            with open(label_file, "w") as file:
                file.writelines(str_yolo_formats)


if __name__ == '__main__':
    main()
