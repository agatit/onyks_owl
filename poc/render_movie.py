import click

import cv2
import json

from tqdm import tqdm

from frame_processing.FrameProcessor import FrameProcessor
from loggers.loggers import init_rich_info_logger
from stitch.rectify.FrameRectifier import ConfigFrameRectifier
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8

logger = init_rich_info_logger(__name__)

rectify_config_formats = {

}

@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select movie to process")
@click.option("-out", "--output", "output_movie",
              required=True, type=click.Path(),
              help="select output directory")
@click.option("-mp", "--model_path", "model_path",
              type=click.Path(exists=True, file_okay=True),
              help="yolov5 model path - .pt")
@click.option("-rc", "--rectify_config", "rectify_config", type=click.Path(exists=True, file_okay=True),
              help=f"rectify config path, supported formats:{rectify_config_formats.keys()}")
@click.option("-fps", "--fps", "fps", type=int,
              default=25, help="movie fps")
@click.option("-re", "--resolution", "resolution", type=(int, int),
              default=(2160, 3840), help="movie pixel resolution e.g. 1920 1080")
@click.option("-c", "--codec", "codec_code", type=str,
              default='mp4v', help="select movie codec")
def main(input_movie, output_movie, model_path, rectify_config, fps, resolution, codec_code):
    """
    Render movie with rectification or object detection.
    """

    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        logger.error("Error opening video stream or file")
        return

    frame_processors: list[FrameProcessor] = []

    codec = cv2.VideoWriter.fourcc(*codec_code)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    frame_rectifier = None
    if rectify_config:
        with open(rectify_config) as f:
            config = json.load(f)

        frame_rectifier = ConfigFrameRectifier(config)
        frame_rectifier.calc_maps()

    detector = YoloDetectorV8(model_path, batch_size=100)
    # classes = [0, 1]
    # detector.select_classes(classes)


    batch = []
    frame_count = int(input_cam.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=frame_count, desc=f"Processing: {input_movie}") as pbar:
        while input_cam.isOpened():
            result, frame = input_cam.read()
            if result:

                if rectify_config:
                    frame = frame_rectifier.rectify(frame)

                if len(batch) < detector.batch_size:
                    batch.append(frame)
                    pbar.update()
                    continue

                detected_frames = detector(batch)
                for frame in write_bounding_boxes_gen(batch, detected_frames):
                    video_writer.write(frame)

                batch = []
                pbar.update()
            else:
                detected_frames = detector(batch)
                for frame in write_bounding_boxes_gen(batch, detected_frames):
                    video_writer.write(frame)

                pbar.update()
                break

    input_cam.release()
    video_writer.release()


def write_bounding_boxes_gen(batch, detected_frames):
    for frame, detection_results in zip(batch, detected_frames):
        for detection_result in detection_results:
            frame = detection_result.draw_on_image(frame)

        yield frame


if __name__ == '__main__':
    main()
