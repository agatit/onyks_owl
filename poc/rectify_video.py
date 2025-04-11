import click

import cv2
import json

from stitch.rectify.FrameRectifier import ConfigFrameRectifier

frame_size = (1920, 1080)


@click.command()
@click.option("-in", "--input_movie", "input_movie",
              required=True, type=click.Path(exists=True),
              help="movie to rectify")
@click.option("-out", "--output_movie", "output_movie",
              required=True, type=click.Path(exists=True),
              help="output rectified video")
@click.option("-rc", "--rectify_config", "rectify_config",
              required=True, type=click.Path(exists=True),
              help="select rectify json file")
@click.option("-s", "--start", "start_frame",
              type=int, default=0,
              help="number of start frame")
@click.option("-e", "--end", "end_frame",
              type=int, default=-1,
              help="number of stop frame")
@click.option("-v", "--verbose", "verbose",
              is_flag=True,
              help="verbose mode")
def main(input_movie, output_movie, rectify_config, display):
    with open(rectify_config) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = ConfigFrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    resolution_scale = config['scale']

    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")

    codec = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 25
    # resolution = (int(1920 * resolution_scale), int(1080 * resolution_scale))
    resolution = (frame_size[0], frame_size[1])
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    print(f"started {input_movie} processing")

    count = 0
    while input_cam.isOpened():
        ret, frame = input_cam.read()
        if ret:
            frame = frame_rectifier.rectify(frame)

            frame = resize_image(frame, frame_size)
            video_writer.write(frame)

            if display:
                display_frame(frame)

            if count % 50 == 0:
                print(f"rendered: {count} frames")

            count = count + 1
        else:
            break

    input_cam.release()
    video_writer.release()


if __name__ == '__main__':
    main()
