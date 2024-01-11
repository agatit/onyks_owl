import click

import cv2
import json

from display.utils import scale_image_by_percent
from stitch.rectify.FrameRectifier import FrameRectifier


def show_rectified_image(image_path, frame_rectifier, save_path, scale_percent):
    image = cv2.imread(image_path)

    rectified = frame_rectifier.rectify(image)

    image = scale_image_by_percent(rectified, scale_percent)
    cv2.imshow('Frame', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if save_path:
        cv2.imwrite(save_path, rectified)


def show_rectified_video(video_path, frame_rectifier, save_path, scale_percent):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:

            frame = frame_rectifier.rectify(frame)
            frame = scale_image_by_percent(frame, scale_percent)
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
@click.option('--image', "action", flag_value="image", help="Input file type flag")
@click.option('--video', "action", flag_value="video", help="Input file type flag")
@click.option('-s', "--save", "save_flag", help="save file path")
@click.option('-sp', '--scale_percent', "scale", default=75)
def main(input_source, config_json, action, save_flag, scale):
    actions = {
        "image": show_rectified_image,
        "video": show_rectified_video
    }

    with open(config_json) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    callback = actions[action]
    callback(input_source, frame_rectifier, save_flag, scale)


if __name__ == '__main__':
    main()
