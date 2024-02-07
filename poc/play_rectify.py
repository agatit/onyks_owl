from pathlib import Path

import click

import json

from stitch.rectify.FrameRectifier import FrameRectifier
from stream.commands.CommandInvoker import CommandInvoker
from stream.Stream import Stream
from stream.commands.display.DestroyWindowsCommand import DestroyWindowsCommand
from stream.commands.display.DisplayImageCommand import DisplayImageCommand
from stream.commands.display.DisplayStreamCommand import DisplayStreamCommand
from stream.commands.display.InterruptStreamCommand import InterruptStreamCommand
from stream.commands.transformation.RectifyCommand import RectifyCommand
from stream.commands.transformation.ScaleImageCommand import ScaleImageCommand
from stream.directors.DisplayImageDirector import DisplayImageDirector
from stream.directors.DisplayStreamDirector import DisplayStreamDirector
from stream.loaders.SingleImageLoader import SingleImageLoader
from stream.loaders.VideoLoader import VideoLoader


@click.command()
@click.option("-in", "--input", "input_source",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="image or video to rectify")
@click.option("-rc", "--rectify_config", "config_json",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="rectify json config")
@click.option('--image', "action", flag_value="image", help="Input file type flag")
@click.option('--video', "action", flag_value="video", help="Input file type flag")
@click.option('-sp', '--scale_percent', "scale", default=60)
def main(input_source, config_json, action, scale):
    with open(config_json) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    input_source_path = Path(input_source)
    if action == "image":
        loader = SingleImageLoader(input_source_path)
        stream = Stream(loader=loader, frame_rectifier=frame_rectifier)

        DisplayImageDirector(stream, scale).run()

    if action == "video":
        loader = VideoLoader(input_source_path)
        stream = Stream(loader=loader, frame_rectifier=frame_rectifier)

        DisplayStreamDirector(stream, scale).run()


if __name__ == '__main__':
    main()
