import click

import cv2
import json

from tqdm import tqdm

from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.yolo_detectors.YoloDetectorV5 import YoloDetectorV5


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select movie to process")
@click.option("-out", "--output", "output_movie",
              required=True, type=click.Path(),
              help="select output directory")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/models/x_owl_4.pt", help="yolov5 model path")
@click.option("-c", "--codec", "codec_code", type=click.Choice(['MJPG', 'mp4v'], case_sensitive=False),
              required=True, default="resources/models/x_owl_4.pt", help="select movie codec")
@click.option("-rc", "--rectify_config", "rectify_config", type=click.Path(exists=True, file_okay=True),
              help="rectify config path")
def main(input_movie, output_movie, model_path, codec_code, rectify_config):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")
        exit(1)

    codec = cv2.VideoWriter_fourcc(*codec_code)
    fps = 25
    resolution = (1920, 1080)
    video_writer = cv2.VideoWriter(output_movie, codec, fps, resolution)

    frame_rectifier = None
    if rectify_config:
        with open(rectify_config) as f:
            config = json.load(f)

        frame_rectifier = FrameRectifier(config)
        frame_rectifier.calc_maps()

    detector = YoloDetectorV5(model_path, batch_size=100)
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
