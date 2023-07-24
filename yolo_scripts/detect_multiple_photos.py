import glob
import logging
import os.path
import pathlib

import click
import cv2
from tqdm import tqdm

from loggers import InfoLogger
from yolo.yolo_detector import YoloDetector

from opencv_tools.image_transformations import show_image_with_rectangles, draw_image_with_rectangles


@click.command()
@click.argument("image_directory")
@click.argument("output_directory", default="output/detect_multiple_photos")
@click.option("--model_path", default="models/l_owl_4.pt")
@click.option("--image_extension", default="jpg")
@click.option("--show_images_boxes", default="False", type=bool)
def main(image_directory, output_directory, model_path, image_extension, show_images_boxes):
    image_directory_mask = pathlib.Path(image_directory).joinpath(f"*.{image_extension}")
    images = glob.glob(str(image_directory_mask), recursive=True)

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    detector = YoloDetector(model_path)

    log_file_name = "log.txt"
    log_path = pathlib.Path(output_directory).joinpath(log_file_name)
    logger = InfoLogger.init(log_path)

    for image_path in tqdm(images, desc="Processed images"):
        image = cv2.imread(image_path)
        found_bounding_boxes = detector.detect_image(image)
        image = draw_image_with_rectangles(image, found_bounding_boxes)

        logger.info(f"{image_path}: {found_bounding_boxes}")

        if show_images_boxes:
            show_image_with_rectangles(image_path, found_bounding_boxes)

        output_file_name = pathlib.Path(image_path).name
        output_file = pathlib.Path(output_directory).joinpath(output_file_name)

        if os.path.exists(output_file):
            os.remove(output_file)

        cv2.imwrite(str(output_file), image)


if __name__ == '__main__':
    main()
