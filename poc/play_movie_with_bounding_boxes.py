from pathlib import Path

import click

from stream.commands.CommandInvoker import CommandInvoker
from stream.Stream import Stream
from stream.commands.detection.DetectImageCommand import DetectImageCommand
from stream.commands.display.DestroyWindowsCommand import DestroyWindowsCommand
from stream.commands.display.DisplayStreamCommand import DisplayStreamCommand
from stream.commands.display.InterruptStreamCommand import InterruptStreamCommand
from stream.commands.transformation.DrawBoundingBoxesCommand import DrawBoundingBoxesCommand
from stream.commands.transformation.ScaleImageCommand import ScaleImageCommand
from stream.loaders.VideoLoader import VideoLoader
from yolo.YoloDetector import YoloDetector


@click.command()
@click.option("-in", "--input", "input_movie",
              required=True, type=click.Path(exists=True),
              help="select movie to display")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/models/s_owl_4.pt", help="yolov5 model path")
@click.option("-sp", "--scale_percent", "scale_percent", type=int, default=50, help="scale view movie")
@click.option("-ct", "--confidence_threshold", "confidence_threshold", type=float, default=0.25,
              help="min confidence of detection")
def main(input_movie, model_path, scale_percent, confidence_threshold):
    video_path = Path(input_movie)
    loader = VideoLoader(video_path)

    yolo_detector = YoloDetector(model_path, confidence_threshold)
    all_labels = yolo_detector.labels

    stream = Stream(loader=loader, yolo_detector=yolo_detector)

    in_stream_invoker = CommandInvoker()
    in_stream_invoker.add_command(DetectImageCommand(stream, all_labels))
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
