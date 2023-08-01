import click

import rectify
import cv2
import json
import numpy as np


def show_rectified_image(image_path):
    image = cv2.imread(image_path)

    frame = rectify.rectify(image)

    cv2.imshow('Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_rectified_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():

        ret, frame = cap.read()
        if ret:

            frame = rectify.rectify(frame)
            cv2.imshow('Frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break
    cv2.destroyAllWindows()
    cap.release()


@click.command()
@click.argument("input_source")
@click.argument("config_json")
@click.option('--image', "action", flag_value="image")
@click.option('--video', "action", flag_value="video")
def main(input_source, config_json, action):
    actions = {
        "image": show_rectified_image,
        "video": show_rectified_video
    }

    with open(config_json) as f:
        rectify.calc_maps(json.load(f), 1920, 1080)

    callback = actions[action]
    callback(input_source)


if __name__ == '__main__':
    main()
