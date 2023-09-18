import click

import cv2
import json

from stitch.rectify.FrameRectifier import FrameRectifier


def scale_image(image, scale):
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def show_rectified_image(image_path, frame_rectifier, scale_percent):
    image = cv2.imread(image_path)

    image = frame_rectifier.rectify(image)

    image = scale_image(image, scale_percent)
    cv2.imshow('Frame', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_rectified_video(video_path, frame_rectifier, scale_percent):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:

            frame = frame_rectifier.rectify(frame)
            frame = scale_image(frame, scale_percent)
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
@click.option('-sp', '--scale_percent', "scale", default=50)
def main(input_source, config_json, action, scale):
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
    callback(input_source, frame_rectifier, scale)


if __name__ == '__main__':
    main()
