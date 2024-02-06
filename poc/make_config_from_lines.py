import json
from pathlib import Path

import click
import yaml
from scipy.optimize import minimize

from display.RegionOfInterest import RegionOfInterest
from io_utils.yaml import literal_to_tuple
from rectify_optimalization.objective_functions.MeanObjectiveFunction import MeanObjectiveFunction
from rectify_optimalization.objective_functions.methods.StdMethod import StdMethod
from rectify_optimalization.objective_functions.methods.line_part_selectors.XPoints import XPoints
from rectify_optimalization.objective_functions.methods.line_part_selectors.YPoints import YPoints
from rectify_optimalization.objective_functions.methods.line_types.Horizontal import Horizontal
from rectify_optimalization.objective_functions.methods.line_types.Vertical import Vertical
from stitch.rectify.FrameRectifier import FrameRectifier
from stream.Stream import Stream
from stream.directors.DisplayImageDirector import DisplayImageDirector
from stream.directors.DisplayStreamDirector import DisplayStreamDirector
from stream.loaders.SingleImageLoader import SingleImageLoader
from stream.loaders.VideoLoader import VideoLoader


@click.command()
@click.option("-in", "--input", "lines_path", type=click.Path(exists=True, file_okay=True),
              required=True, help="json file with lines")
@click.option("-out", "--output", "output_path", type=click.Path(),
              required=True, help="json rectify config")
@click.option("-cf", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/make_config_from_lines.yaml", help="yaml config")
@click.option("-img", "--image", "image_path", type=click.Path(exists=True, file_okay=True),
              help="display image to rectify")
@click.option("-mv", "--movie", "movie_path", type=click.Path(exists=True, file_okay=True),
              help="display movie to rectify")
@click.option("-d", "--display_ratio", "display_ratio", type=int, default=60,
              help="display images in x% ratio")
def main(lines_path, output_path, config_path, image_path, movie_path, display_ratio):
    with open(lines_path, "r") as file:
        lines = json.load(file)

    with open(config_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    consts = config["consts"]
    region_size = (consts["width"], consts["height"])
    roi = RegionOfInterest(region_size, **config["roi"])

    horizontal_method = StdMethod(lines, 1, Horizontal(), YPoints(), roi)
    vertical_method = StdMethod(lines, 1, Vertical(), XPoints(), roi)

    objective_function = MeanObjectiveFunction(consts, horizontal_method, vertical_method)
    function_to_minimize = objective_function.get_function_to_optimize()

    x0 = list(config["init_values"].values())
    minimize_params = init_minimize_params(config)
    res = minimize(function_to_minimize, x0, **minimize_params)

    init_guess = function_to_minimize(x0)
    print("init guess fun value:", init_guess)
    print(res)
    if res.success:

        rectify_config = objective_function.make_rectify_config(res)

        with open(output_path, "w") as file:
            json.dump(rectify_config, file)

        print(rectify_config)

        frame_rectifier = None
        if movie_path or image_path:
            frame_rectifier = FrameRectifier(rectify_config, *region_size)
            frame_rectifier.calc_maps()

        if image_path:
            loader = SingleImageLoader(Path(image_path))
            stream = Stream(loader=loader, frame_rectifier=frame_rectifier)

            DisplayImageDirector(stream).run()

        if movie_path:
            loader = VideoLoader(Path(movie_path))
            stream = Stream(loader=loader, frame_rectifier=frame_rectifier)

            DisplayStreamDirector(stream).run()


def init_minimize_params(config: dict) -> dict:
    minimize_params = config["minimize_params"]
    minimize_params["bounds"] = init_bounds(config)
    return minimize_params


def init_bounds(config: dict) -> list:
    config["bounds"] = literal_to_tuple(config["bounds"], config["bounds"].keys())
    bounds = list(config["bounds"].values())
    return bounds


if __name__ == '__main__':
    main()