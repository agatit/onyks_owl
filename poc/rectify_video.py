import click

import rectify
import cv2
import json


@click.command()
@click.argument("input_movie")
@click.argument("output_movie")
@click.argument("config_json")
def main(input_movie, output_movie, config_json):
    with open(config_json) as f:
        rectify.calc_maps(json.load(f), 1920, 1080)

    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")

    codec = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 25
    resolution = (1920, 1080)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    print(f"started {input_movie} processing")

    count = 0
    while input_cam.isOpened():
        ret, frame = input_cam.read()
        if ret:
            frame = rectify.rectify(frame)
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
