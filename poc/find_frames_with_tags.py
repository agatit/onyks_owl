import dataclasses
import glob
import json
import os
from functools import partial
from pathlib import Path
from typing import Iterable, Callable

import click
import yaml
from tqdm import tqdm

from find_frames_with_tags_scripts.ProcessFrameData import ProcessFrameData
from find_frames_with_tags_scripts.loaders import load_efficientnet, load_any_below_threshold, \
    load_exporter_original_image, load_exporter_bounding_box_image, load_exporter_cropped, load_tracking_patience
from find_frames_with_tags_scripts.process import process
from io_utils.utils import make_clean_dir
from io_utils.yaml import init_options, Options
from stitch.rectify.FrameRectifier import ConfigFrameRectifier
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select directory with movies_paths")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              help="select output directory for measurements")
@click.option("-c", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/find_frames_with_tags.yaml", help="yaml config path")
@click.option("-rc", "--rectify_config", "rectify_config_path", type=click.Path(exists=True, file_okay=True),
              help="rectify config path")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/models/s_owl_4.pt", help="yolov5 model path")
def main(input_dir, output_dir, config_path, rectify_config_path, model_path):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    rectify_config = {}
    if rectify_config_path:
        with open(rectify_config_path) as f:
            rectify_config = json.load(f)

    make_clean_dir(output_dir)

    process_data = configure_process_data(config, input_dir, model_path, output_dir, rectify_config)

    for data in process_data:
        for _ in tqdm(process(data), desc=data.movie_path.name):
            pass

    outputs = {}
    for data in process_data:
        movie_name = data.movie_path.stem
        output_data = [dataclasses.asdict(i) for i in data.output_data]

        outputs[movie_name] = output_data

    output_file = output_dir / "output.json"
    with open(str(output_file), 'w') as file:
        json.dump(outputs, file)


def configure_process_data(config, input_dir, model_path, output_dir, rectify_config):
    input_extension = config["extension"]["input"]
    movies_paths = init_movie_paths(input_dir, input_extension)

    confidence_threshold = float(config["model"]["confidence_threshold"])
    batch = config["model"]["batch"]
    labels_id = config["model"]["classes"]
    detector = YoloDetectorV8(model_path, confidence_threshold, batch)
    detector.select_classes(labels_id)

    batch_filters: Options = {
        "efficientnet": load_efficientnet,
    }
    detection_filters: Options = {
        "any_below_threshold": load_any_below_threshold,
        "tracking_patience": load_tracking_patience
    }
    export_frame_callbacks: Options = {
        "original_image": load_exporter_original_image,
    }
    export_frame_with_detections_callbacks: Options = {
        "cropped": load_exporter_cropped,
        "bounding_box_image": load_exporter_bounding_box_image
    }

    batch_filters = init_options(batch_filters, config["batch_filters"])
    detection_filters = init_options(detection_filters, config["detections_filters"])
    export_frame_callbacks = init_options(export_frame_callbacks, config["output"])
    export_frame_with_detections_callbacks = init_options(export_frame_with_detections_callbacks, config["output"])

    frame_size = config["image_size"]["width"], config["image_size"]["height"]
    output_extension = config["extension"]["output"]
    empty_image_step = config["empty_image_step"]

    process_data = []
    for movie_path in movies_paths:
        frame_rectifier = None

        if len(rectify_config) > 0:
            frame_rectifier = ConfigFrameRectifier(rectify_config, *frame_size)
            frame_rectifier.calc_maps()

        _output_dir = output_dir / movie_path.stem
        os.mkdir(_output_dir)

        new_data = ProcessFrameData(movie_path, _output_dir, output_extension,
                                    frame_rectifier, detector, empty_image_step)

        new_data.batch_filter_callbacks = batch_filters
        new_data.detections_filter_callbacks = detection_filters

        add_callbacks_to_list_partial = partial(add_callbacks_to_list, new_data)
        add_callbacks_to_list_partial(new_data.export_frame_callbacks, export_frame_callbacks)
        add_callbacks_to_list_partial(new_data.export_frame_with_detections_callbacks,
                                      export_frame_with_detections_callbacks)

        process_data.append(new_data)

    return process_data


def add_callbacks_to_list(process_frame_data: ProcessFrameData, target_list: list, callbacks: Iterable[Callable]):
    for callback in callbacks:
        partial_fun = partial(callback, process_frame_data)
        target_list.append(partial_fun)


def init_movie_paths(input_dir: Path, input_extension: str) -> list[Path]:
    glob_mask = input_dir / f"*{input_extension}"
    movies_paths = glob.glob(str(glob_mask))

    return [Path(i) for i in movies_paths]


if __name__ == '__main__':
    main()
