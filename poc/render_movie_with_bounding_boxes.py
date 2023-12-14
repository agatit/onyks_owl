import click

import cv2
import json

import numpy as np

from opencv_tools.image_transformations import draw_image_with_rectangles
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.yolo_detector import YoloDetector


@click.command()
@click.argument("input_movie")
@click.argument("output_movie")
@click.argument("rectify_config")
@click.argument("model_path", default="models/l_owl_4.pt")
def main(input_movie, output_movie, rectify_config, model_path):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")
        exit(1)

    codec = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 25
    resolution = (1920, 1080)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    with open(rectify_config) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    detector = YoloDetector(model_path)

    print(f"started {input_movie} processing to {output_movie}")

    count = 0
    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:
            frame = frame_rectifier.rectify(frame)

            found_bounding_boxes = detector.detect_image(frame)
            frame = draw_image_with_rectangles(frame, found_bounding_boxes)

            video_writer.write(frame)

            if count % 50 == 0:
                print(f"rendered: {count} frames")

            count = count + 1
        else:
            break

    input_cam.release()
    video_writer.release()


if __name__ == '__main__':
    main()
