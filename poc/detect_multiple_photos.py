import glob
import json
import logging
import os.path
import pathlib

import click
import cv2
from tqdm import tqdm

from loggers.loggers import InfoLogger
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.YoloDetector import YoloDetector

from opencv_tools.image_transformations import show_image_with_rectangles, draw_image_with_rectangles


@click.command()
@click.option("-in", "--input", "image_directory",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select image directory")
@click.option("-out", "--output", "output_directory",
              required=True, type=click.Path(),
              help="select output directory")
@click.option("--rectify_config", required=True, type=click.Path(exists=True, file_okay=True))
@click.option("--model_path", required=True, default="models/l_owl_4.pt")
@click.option("--image_extension", required=True, default="jpg")
@click.option("--show_images_boxes", required=True, default="False", type=bool)
def main(image_directory, output_directory, rectify_config, model_path, image_extension, show_images_boxes):
    with open(rectify_config) as f:
        rectify_config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(rectify_config, *frame_size)
    frame_rectifier.calc_maps()

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
        image = frame_rectifier.rectify(image)

        found_bounding_boxes = detector.detect_image(image, detector.labels)
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
