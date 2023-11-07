import dataclasses
import json
import os.path
from itertools import product

import click
import numpy as np
import yaml
from scipy.optimize import minimize
from tqdm import tqdm

from display.Points import PointStyle, display_image_with_points, PointDisplay
from io_utils.yaml import tuple_to_literal
from rectify_optimalization.Measurement import Measurement
from rectify_optimalization.Result import Result
from rectify_optimalization.objective_function import objective_function, calc_horizontal_std, calc_vertical_std, \
    calc_horizontal_distance


def make_config_from_res(res, consts):
    return {
        'sensor_h': consts["sensor_h"],
        'sensor_w': consts["sensor_w"],
        'X': res.x[0],
        'Y': res.x[1],
        'alpha': res.x[2],
        'beta': res.x[3],
        'gamma': res.x[4],
        'focus': res.x[5],
        'scale': res.x[6],
        'dist': res.x[7:].tolist()
    }


def display(display_ratio, measurements):
    horizontal_style = PointStyle(5, -1, (250, 0, 0))
    vertical_style = PointStyle(5, -1, (0, 0, 255))
    for measurement in measurements:
        points_displays = [
            PointDisplay(measurement.horizontal_lines, horizontal_style),
            PointDisplay(measurement.vertical_lines, vertical_style)
        ]
        image = measurement.load_image()
        name = measurement.name
        display_image_with_points(image, name, display_ratio, *points_displays)


@click.command()
@click.option("-cf'", "--config", "rectify_optimization_config", default="resources/rectify_optimization.yaml",
              required=True, type=click.Path(exists=True), help="yaml configuration for tests")
@click.option("-out", "--output", "output", type=click.Path(exists=True),
              required=True, help="output directory for measurements")
@click.option("-d", "--display_ratio", "display_ratio", type=int,
              help="display images in x% ratio")
def main(rectify_optimization_config, output, display_ratio):
    with open(rectify_optimization_config, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config["bounds"] = tuple_to_literal(config["bounds"], config["bounds"].keys())

    measurements = []
    for measurement in config["measurements"]:
        new_line = Measurement(**measurement)
        new_line.load_lines()
        measurements.append(new_line)

    if display_ratio:
        display(display_ratio, measurements)

    x0 = np.array(list(config["init_values"].values()))
    bounds_list = list(config["bounds"].values())

    stds = next(filter(lambda x: x.name == "wagon", measurements))
    distances = next(filter(lambda x: x.name == "szyny", measurements))

    weights_range = {
        "stds": np.arange(*config["weights_range"]["stds"]),
        "distances": np.arange(*config["weights_range"]["distances"])
    }

    results = []
    weights_list = list(product(weights_range["stds"], weights_range["distances"]))
    for w_std, w_distance in tqdm(weights_list):
        weights = {
            "std": w_std,
            "distance": w_distance
        }
        consts = config["consts"].copy()
        consts["weights"] = weights

        minimize_params = {
            "method": "nelder-mead",
            "args": (consts, stds.horizontal_lines, stds.vertical_lines, distances.horizontal_lines),
            "bounds": bounds_list,
            "options": {'disp': False, "maxiter": 50000},
            # "tol": 0.1
        }

        res = minimize(objective_function, x0, **minimize_params)
        res_config = res.x

        standard_deviations = {
            "horizontal": calc_horizontal_std(res_config, consts, stds.horizontal_lines).sum(),
            "vertical": calc_vertical_std(res_config, consts, stds.vertical_lines).sum(),
            "distance": calc_horizontal_distance(res_config, consts, distances.horizontal_lines).sum(),
        }
        result_params = {
            "name": f"{w_std}x{w_distance}",
            "res": {"result": res.fun, "iterations": res.nit},
            "weights": weights,
            "standard_deviations": standard_deviations,
            "config": make_config_from_res(res, consts)
        }
        new_result = Result(**result_params)
        results.append(new_result)

    output_json = {
        "bounds": config["bounds"],
        "results": [dataclasses.asdict(i) for i in results]
    }

    try:
        output_path = os.path.join(output, "output.json")
        with open(output_path, "w") as file:
            json.dump(output_json, file)
        print(f"saved to: {output_path}")
    except Exception as e:
        print(e)
        print(json.dumps(output_json))



if __name__ == '__main__':
    main()
