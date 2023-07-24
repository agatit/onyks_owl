import glob
import itertools
from pathlib import Path

import click

from src.opencv_tools.image_transformations import show_image_with_rectangles
from yolo.yolo_detector import YoloDetector


@click.command()
@click.argument("models_directory")
@click.argument("images_directory")
def main(models_directory, images_directory):
    glob_mask = Path(models_directory).joinpath('*')
    models_paths = glob.glob(str(glob_mask))

    glob_mask = Path(images_directory).joinpath('*.jpg')
    test_images_paths = glob.glob(str(glob_mask), recursive=True)

    detectors = [YoloDetector(path) for path in models_paths]

    for detector, image_path in itertools.product(detectors, test_images_paths):
        print(detector.model_path, image_path)

        found_bounding_boxes = detector.detect_image(image_path)
        print(found_bounding_boxes)

        show_image_with_rectangles(image_path, found_bounding_boxes)
        print("\n\n\n")


if __name__ == '__main__':
    main()
