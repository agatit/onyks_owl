import json
import logging
import os
import shutil
from pathlib import Path
import click
import cv2

from io_utils.utils import make_clean_dir
from stitch.rectify.FrameRectifier import ConfigFrameRectifier

def frame_capture_gen(film_path):
    vid_obj = cv2.VideoCapture(film_path)

    success = 1
    while success:
        success, image = vid_obj.read()
        if success:
            yield image



@click.command()
@click.option("-in", "--input_movie", "input_movie",
              required=True, type=click.Path(exists=True),
              help="source movie")
@click.option("-out", "--output_dir", "output_dir",
              required=True, type=click.Path(),
              help="directory to save frames")
@click.option("-rc", "--rectify_config", "rectify_config", type=click.Path(exists=True, file_okay=True),
              help="rectify config path")
@click.option("-ie", "--image_extension", "image_extension", type=str,
              default=".jpg", help="image extension with dot")
@click.option("-v", "--verbose", "verbose", is_flag=True,
              help="enable verbose mode")
def main(input_movie, output_dir, rectify_config, image_extension, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)

    input_movie = Path(input_movie)
    output_dir = Path(output_dir)

    make_clean_dir(output_dir)

    frame_rectifier = None
    if rectify_config:
        with open(rectify_config) as f:
            rectify_config = json.load(f)
        frame_rectifier = ConfigFrameRectifier(rectify_config)
        frame_rectifier.calc_maps()

    logging.info(f"Started: {input_movie}")
    for index, frame in enumerate(frame_capture_gen(str(input_movie))):
        file_name = f"frame_{index}{image_extension}"
        file_path = Path(output_dir) / file_name

        if frame_rectifier:
            frame = frame_rectifier.rectify(frame)

        cv2.imwrite(str(file_path), frame)

        if index % 50 == 0:
            logging.info(f"processed: {index}")


if __name__ == '__main__':
    main()
