from pathlib import Path

import click

import cv2
import json

import numpy as np

from opencv_tools.image_transformations import draw_image_with_rectangles
from yolo.yolo_detector import YoloDetector


@click.command()
@click.argument("input_movie")
@click.argument("model_path", default="models/l_owl_4.pt")
def main(input_movie, model_path):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")
        exit(1)
    input_movie_name = Path(input_movie).name

    detector = YoloDetector(model_path)

    print(f"started processing: {input_movie}")

    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:
            found_bounding_boxes = detector.detect_image(frame)
            frame = draw_image_with_rectangles(frame, found_bounding_boxes)

            detector.model.track()
            cv2.imshow(input_movie_name, frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    input_cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
