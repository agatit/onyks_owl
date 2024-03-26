import json
from pathlib import Path

import click

from stitch.rectify.FrameRectifier import FrameRectifier
from stream.commands.CommandInvoker import CommandInvoker
from stream.Stream import Stream
from stream.commands.detection.DetectImageCommand import DetectImageCommand
from stream.commands.display.DestroyWindowsCommand import DestroyWindowsCommand
from stream.commands.display.DisplayStreamCommand import DisplayStreamCommand
from stream.commands.display.InterruptStreamCommand import InterruptStreamCommand
from stream.commands.transformation.DrawBoundingBoxesCommand import DrawBoundingBoxesCommand
from stream.commands.transformation.RectifyCommand import RectifyCommand
from stream.commands.transformation.ScaleImageCommand import ScaleImageCommand
from stream.loaders.VideoLoader import VideoLoader
from yolo.yolo_detectors.YoloDetectorV5 import YoloDetectorV5
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8

yolo_versions = {
    "v5": YoloDetectorV5,
    "v8": YoloDetectorV8
}


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True),
              help="select movie to display")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, help="yolov5 model path")
@click.option("-rc", "--rectify_config", "rectify_config", type=click.Path(exists=True, file_okay=True),
              required=True, help="rectify json file")
@click.option("-v", "--yolo_version", "yolo_version", type=click.Choice(yolo_versions.keys()),
              required=True, help="select yolo version")
@click.option("-sp", "--scale_percent", "scale_percent", type=int, default=50, help="scale view movie")
@click.option("-ct", "--confidence_threshold", "confidence_threshold", type=float, default=0.25,
              help="min confidence of detection")
def main(input_movie, model_path, rectify_config, yolo_version, scale_percent, confidence_threshold):
    video_path = Path(input_movie)
    loader = VideoLoader(video_path)

    frame_rectifier = None
    if rectify_config:
        with open(rectify_config) as f:
            config = json.load(f)

        frame_size = (1920, 1080)
        frame_rectifier = FrameRectifier(config, *frame_size)
        frame_rectifier.calc_maps()

    detector_class = yolo_versions[yolo_version]
    yolo_detector = detector_class(model_path, confidence_threshold)

    stream = Stream(loader=loader, yolo_detector=yolo_detector, frame_rectifier=frame_rectifier)

    in_stream_invoker = CommandInvoker()

    if rectify_config:
        in_stream_invoker.add_command(RectifyCommand(stream))

    in_stream_invoker.add_command(DetectImageCommand(stream))
    in_stream_invoker.add_command(DrawBoundingBoxesCommand(stream))
    in_stream_invoker.add_command(ScaleImageCommand(stream, scale_percent))
    in_stream_invoker.add_command(DisplayStreamCommand(stream))
    in_stream_invoker.add_command(InterruptStreamCommand(stream))

    post_stream_invoker = CommandInvoker()
    post_stream_invoker.add_command(DestroyWindowsCommand(stream))

    for _ in stream.get_next_frame_gen():
        in_stream_invoker.invoke()

    post_stream_invoker.invoke()


if __name__ == '__main__':
    main()
