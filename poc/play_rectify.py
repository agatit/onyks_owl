import pickle
from pathlib import Path
import click
import json
import cv2

from display.utils import scale_image_by_percent
from loggers.loggers import init_default_info_logger
from stitch.rectify.FrameRectifier import ConfigFrameRectifier

logger = init_default_info_logger(__name__)

input_types = [
    "video", "image"
]

rectification_sources = [
    "config", "mapx_mapy"
]


@click.command()
@click.option("-in", "--input", "input_source",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="media to rectify")
@click.option("-int", "--input_type", "input_type",
              required=True, type=click.Choice(input_types),
              help="input file type")
@click.option("-r", "--rectify_config", "rectify_config",
              required=True, type=click.Path(exists=True),
              help="rectify config file")
@click.option("-rs", "--rectification_source", "rectification_source",
              required=True, type=click.Choice(rectification_sources),
              help="rectification source")
@click.option('-sp', '--scale_percent', "scale", default=60)
@click.option('-fs', '--frame_size', "frame_size", type=(int, int), default=(1920, 1080),
              help="frame size - width x height")
def main(input_source, input_type, rectify_config, rectification_source, scale, frame_size):
    """
    Rectify and display input media.
    """
    logger.info(f"started: {__file__}")

    frame_rectifier = None
    if rectification_source == "config":
        with open(rectify_config) as f:
            config = json.load(f)

        frame_rectifier = ConfigFrameRectifier(config, *frame_size)
        frame_rectifier.calc_maps()

    elif rectification_source == "mapx_mapy":
        with open(rectify_config, "rb") as file:
            loaded_data = pickle.load(file)

        frame_rectifier = ConfigFrameRectifier({}, *frame_size)
        frame_rectifier.map_x = loaded_data["mapx"]
        frame_rectifier.map_y = loaded_data["mapy"]

    input_source_path = Path(input_source)
    if input_type == "image":
        input_path_str = str(input_source_path)
        image = cv2.imread(input_path_str)

        rectified = frame_rectifier.rectify(image)
        rectified_image = scale_image_by_percent(rectified, scale)
        cv2.imshow('original', rectified_image)
        key = cv2.waitKey(0)

        # loader = SingleImageLoader(input_source_path)
        # stream = Stream(loader=loader, frame_rectifier=frame_rectifier)
        #
        # DisplayImageDirector(stream, scale).run()

    if input_type == "video":

        input_path_str = str(input_source_path)
        video_capture = cv2.VideoCapture(input_path_str)

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if ret:
                rectified = frame_rectifier.rectify(frame)
                rectified_image = scale_image_by_percent(rectified, scale)
                # rectified_image = scale_image_by_percent(frame, scale)
                cv2.imshow('original', rectified_image)
                key = cv2.waitKey(1)

                if key == ord('q'):
                    break
            else:
                break

        video_capture.release()
        # loader = VideoLoader(input_source_path)
        # stream = Stream(loader=loader, frame_rectifier=frame_rectifier)
        #
        # DisplayStreamDirector(stream, scale).run()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
