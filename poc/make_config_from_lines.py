import json

import click
import cv2
import yaml
from scipy.optimize import minimize

from display.RegionOfInterest import RegionOfInterest
from display.utils import scale_image_by_percent
from io_utils.yaml import literal_to_tuple
from rectify_optimalization.full_config_objective_functions.MeanObjectiveFunction import MeanFullConfigObjectiveFunction
from rectify_optimalization.methods.StdMethod import StdMethod
from rectify_optimalization.methods.line_part_selectors.XPoints import XPoints
from rectify_optimalization.methods import YPoints
from rectify_optimalization.methods.line_types.Horizontal import Horizontal
from rectify_optimalization.methods.line_types.Vertical import Vertical
from rectify_optimalization.utils import concat_lines
from stitch.rectify.FrameRectifier import ConfigFrameRectifier


@click.command()
@click.option("-in", "--input", "lines_paths", type=click.Path(exists=True, file_okay=True),
              required=True, help="json file with lines, can input multiple", multiple=True)
@click.option("-out", "--output", "output_path", type=click.Path(),
              required=True, help="json rectify config")
@click.option("-cf", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="make_config_from_lines.yaml", help="yaml config")
@click.option("-img", "--image", "image_path", type=click.Path(exists=True, file_okay=True),
              help="display image to rectify")
@click.option("-mv", "--movie", "movie_path", type=click.Path(exists=True, file_okay=True),
              help="display movie to rectify")
@click.option("-d", "--display_ratio", "display_ratio", type=int, default=50,
              help="display images in x% ratio")
def main(lines_paths, output_path, config_path, image_path, movie_path, display_ratio):
    lines = []
    for path in lines_paths:
        with open(path, "r") as file:
            lines.append(json.load(file))

    lines = concat_lines(lines)

    with open(config_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    consts = config["consts"]
    region_size = (consts["width"], consts["height"])
    roi = RegionOfInterest(region_size, **config["roi"])

    horizontal_method = StdMethod(lines, 1, Horizontal(), YPoints(), roi)
    vertical_method = StdMethod(lines, 1, Vertical(), XPoints(), roi)

    objective_function = MeanFullConfigObjectiveFunction(consts, horizontal_method, vertical_method)
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

        if not movie_path and not image_path:
            return

        frame_rectifier = ConfigFrameRectifier(rectify_config, *region_size)
        frame_rectifier.calc_maps()

        if image_path:
            image = cv2.imread(image_path)
            rectified_image = frame_rectifier.rectify(image)
            rectified_image = scale_image_by_percent(rectified_image, display_ratio)
            cv2.imshow('original', rectified_image)
            key = cv2.waitKey(0)

            cv2.destroyAllWindows()
            # loader = SingleImageLoader(Path(image_path))
            # stream = Stream(loader=loader, frame_rectifier=frame_rectifier)
            #
            # DisplayImageDirector(stream).run()

        # if movie_path:
        #     loader = VideoLoader(Path(movie_path))
        #     stream = Stream(loader=loader, frame_rectifier=frame_rectifier)
        #
        #     DisplayStreamDirector(stream).run()


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
