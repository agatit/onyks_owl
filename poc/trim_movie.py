import logging

import av
import av.stream
import av.video
import click
import cv2
from av.video.stream import VideoStream

from av_wrapper.InputStream import InputStream
from av_wrapper.OutputStream import OutputStream

logger = logging.getLogger(__name__)


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True, file_okay=True),
              help="path to input movie")
@click.option("-out", "--output", "output_movie",
              required=True, type=click.Path(),
              help="path to output movie")
@click.option("-s", "--start", "start_frame",
              type=int, default=0,
              help="number of start frame")
@click.option("-e", "--end", "end_frame",
              type=int, default=-1,
              help="number of stop frame")
@click.option("-v", "--verbose", "verbose",
              is_flag=True,
              help="verbose mode")
def main(input_movie, output_movie, start_frame, end_frame, verbose):
    if verbose:
        logging.basicConfig(level=logging.INFO)

    input_stream = InputStream(
        movie_path=input_movie
    )

    output_stream = OutputStream(
        movie_path=output_movie,
        width=input_stream.width,
        height=input_stream.height,
        fps=input_stream.fps
    )

    width = input_stream.width
    height = input_stream.height

    frames = 0
    output_stream.open()
    for raw_frame in input_stream.open():

        if frames < start_frame:
            frames += 1
            continue

        logger.info(f"frame: {frames:05d}")
        frames += 1

        if frames > end_frame > 0:
            break

        if logger.level <= logging.INFO:
            curr_frame = raw_frame.to_ndarray(format="bgr24")
            resized_frame = cv2.resize(curr_frame, (width // 2, height // 2))
            cv2.imshow("f", resized_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        output_stream.write(raw_frame)

    output_stream.close()


if __name__ == '__main__':
    main()

