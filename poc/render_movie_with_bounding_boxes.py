import click

import cv2
import json

import numpy as np
from tqdm import tqdm

from opencv_tools.image_transformations import draw_image_with_rectangles
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.YoloDetector import YoloDetector


# todo: zmienic na folder
@click.command()
@click.argument("input_movie")
@click.argument("output_movie")
@click.option("-rc", "--rectify_config", "rectify_config", type=click.Path(exists=True, file_okay=True),
              help="rectify config path")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/models/x_owl_4.pt", help="yolov5 model path")
@click.option("-c", "--codec", "codec_code", type=click.Choice(['MJPG', 'mp4v'], case_sensitive=False),
              required=True, default="resources/models/x_owl_4.pt", help="yolov5 model path")
def main(input_movie, output_movie, rectify_config, model_path, codec_code):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")
        exit(1)

    codec = cv2.VideoWriter_fourcc(*codec_code)
    fps = 25
    resolution = (1920, 1080)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    # todo: usuniecie ifa
    frame_rectifier = None
    if rectify_config:
        with open(rectify_config) as f:
            config = json.load(f)

        frame_rectifier = FrameRectifier(config)
        frame_rectifier.calc_maps()

    detector = YoloDetector(model_path)

    frame_count = int(video_writer.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=frame_count, desc=f"Processing: {input_movie}") as pbar:
        while input_cam.isOpened():
            result, frame = input_cam.read()
            if result:

                if rectify_config:
                    frame = frame_rectifier.rectify(frame)

                found_bounding_boxes = detector.detect_image(frame)
                frame = draw_image_with_rectangles(frame, found_bounding_boxes)

                video_writer.write(frame)

                pbar.update()
            else:
                break

    input_cam.release()
    video_writer.release()


if __name__ == '__main__':
    main()
