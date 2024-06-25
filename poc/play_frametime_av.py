import av
import av.stream
import av.video
import click
import cv2
import numpy as np


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True, file_okay=True),
              help="path to movie")
@click.option("-s", "--stop", "stop_frame",
              type=int, default=-1,
              help="number of stop frame")
def main(input_movie, stop_frame):
    in_cont = av.open(input_movie)

    fps = in_cont.streams.video[0].base_rate
    width = in_cont.streams.video[0].width
    height = in_cont.streams.video[0].height
    in_stream = in_cont.streams.video[0]

    frames = 0
    time_offset = None
    calc_timestamp = - 1 / fps

    for raw_frame in in_cont.decode(video=0):
        curr_frame = raw_frame.to_ndarray(format="bgr24")

        if time_offset is None:
            time_offset = raw_frame.time

        timestamp = raw_frame.time - time_offset
        calc_timestamp += 1 / fps

        print(f"{frames:05d}: {timestamp - calc_timestamp:.2f}")
        frames += 1

        if frames > stop_frame > 0:
            break

        resized_frame = cv2.resize(curr_frame, (width // 2, height // 2))
        cv2.imshow("f", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    in_cont.close()


if __name__ == '__main__':
    main()
