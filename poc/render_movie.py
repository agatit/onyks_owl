from functools import partial

import click
import cv2
from tqdm import tqdm

from frame_processing import FrameProcessor
from frame_processing.yolo_detection import detect_batch_frames
from frame_processing.rectification import rectify_batch_frames
from loggers.loggers import init_rich_info_logger
from stitch.rectify.FrameRectifier import ConfigFrameRectifier, RawFrameRectifier
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8

logger = init_rich_info_logger(__name__)

rectify_config_formats = {
    "config": ConfigFrameRectifier,
    "mapx_mapy": RawFrameRectifier
}


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True),
              help="select movie to process")
@click.option("-out", "--output", "output_movie",
              required=True, type=click.Path(),
              help="select output directory")
@click.option("-mp", "--model_path", "model_path",
              type=click.Path(exists=True, file_okay=True),
              help="yolo model path - .pt")
@click.option("-rc", "--rectify_config", "rectify_config",
              type=click.Path(exists=True, file_okay=True),
              help=f"rectify config path")
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
    logger.info(f"started: {__file__}")

    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        logger.error("Error opening video stream or file")
        return

    frame_processors: list[FrameProcessor] = []

    codec = cv2.VideoWriter.fourcc(*codec_code)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    if rectify_config:
        for name, frame_rectifier_class in rectify_config_formats.items():
            try:
                frame_rectifier = frame_rectifier_class.load_from_file(rectify_config)
            except Exception as e:
                continue

            logger.info(f"Loaded rectify {name}: {rectify_config}")

            frame_processor = partial(rectify_batch_frames, frame_rectifier=frame_rectifier)
            frame_processors.append(frame_processor)

    batch = []
    batch_size = 100
    if model_path:
        # classes = [0, 1]
        # detector.select_classes(classes)

        detector = YoloDetectorV8(model_path, batch_size=batch_size)

        frame_processor = partial(detect_batch_frames, detector=detector)
        frame_processors.append(frame_processor)

    frame_count = int(input_cam.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=frame_count, desc=f"Processing: {input_movie}") as pbar:
        while input_cam.isOpened():
            result, frame = input_cam.read()

            if result:
                if len(batch) < batch_size:
                    batch.append(frame)
                    pbar.update()
                    continue

                for processor in frame_processors:
                    batch = processor(batch)

                for frame in batch:
                    video_writer.write(frame)

                batch = []
                pbar.update()

            else:
                for processor in frame_processors:
                    batch = processor(batch)

                for frame in batch:
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
