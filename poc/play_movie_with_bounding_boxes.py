from pathlib import Path

import click

import cv2
import json

import numpy as np

from display.utils import scale_image_by_percent
from opencv_tools.image_transformations import draw_image_with_rectangles
from yolo.YoloDetector import YoloDetector


@click.command()
@click.argument("input_movie")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/models/s_owl_4.pt", help="yolov5 model path")
@click.option("-sp", "--scale_percent", "scale_percent", type=int, default=50, help="scale view movie")
@click.option("-ct", "--confidence_threshold", "confidence_threshold", type=float, default=0.25,
              help="min confidence of detection")
def main(input_movie, model_path, scale_percent, confidence_threshold):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")
        exit(1)
    input_movie_name = Path(input_movie).name

    detector = YoloDetector(model_path, confidence_threshold)

    print(f"started processing: {input_movie}")

    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:
            detection_results = detector.detect_image(frame, detector.labels)

            for detection_result in detection_results:
                frame = detection_result.draw_on_image(frame)

            # detector.model.track()
            frame = scale_image_by_percent(frame, scale_percent)
            cv2.imshow(input_movie_name, frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break
        else:
            break

    input_cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
