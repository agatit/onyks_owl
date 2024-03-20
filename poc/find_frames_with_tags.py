import dataclasses
import glob
import json
import os
from functools import partial
from pathlib import Path
from typing import Callable

import click
import torch
import yaml
from tqdm import tqdm

from find_frames_with_tags_scripts.ProcessFrameData import ProcessFrameData
from find_frames_with_tags_scripts.fitering import similarity_conv, filter_batch
from find_frames_with_tags_scripts.process import process, export_original_image, export_cropped_class, \
    export_bounding_box_image, rectify_frame
from io_utils.utils import make_clean_dir
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.YoloDetector import YoloDetector


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

    input_extension = config["extension"]["input"]
    movies_paths = init_movie_paths(input_dir, input_extension)

    confidence_threshold = float(config["model"]["confidence_threshold"])
    batch = config["batch"]
    labels_id = config["labels"].keys()
    detector = YoloDetector(model_path, confidence_threshold, batch)
    detector.select_classes(labels_id)

    frame_size = config["image_size"]["width"], config["image_size"]["height"]
    output_extension = config["extension"]["output"]

    export_callbacks: dict[str, tuple[str, Callable]] = {
        "original_image": ("export_original_image_fun", export_original_image),
        "cropped": ("export_cropped_class_fun", export_cropped_class),
        "bounding_box_image": ("export_bounding_box_image_fun", export_bounding_box_image)
    }
    selected_output = config["output"]
    export_callbacks = [v for k, v in export_callbacks.items() if selected_output[k]]

    empty_image_step = config["empty_image_step"]
    process_data = init_processing_data(frame_size, detector,
                                        movies_paths, output_dir,
                                        rectify_config, output_extension,
                                        export_callbacks, empty_image_step)

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


# todo: zredukować parametry
def init_processing_data(frame_size, detector, movies_paths,
                         output_dir, rectify_config, output_extension,
                         export_callbacks, empty_image_step):
    output = []

    for movie_path in movies_paths:
        frame_rectifier = None
        if len(rectify_config) > 0:
            frame_rectifier = FrameRectifier(rectify_config, *frame_size)
            frame_rectifier.calc_maps()

        _output_dir = output_dir / movie_path.stem
        os.mkdir(_output_dir)

        process_frame_data = ProcessFrameData(movie_path, _output_dir, output_extension,
                                              frame_rectifier, detector, empty_image_step)

        if process_frame_data.rectifier:
            rectify_fun = partial(rectify_frame, process_frame_data)
            process_frame_data.rectify_frame_fun = rectify_fun

        for method_name, callback, in export_callbacks:
            similarity_fun = partial(callback, process_frame_data)
            setattr(process_frame_data, method_name, similarity_fun)

        model, device = load_efficientnet()
        similarity_fun = partial(similarity_conv, model=model, device=device)
        filter_fun = partial(filter_batch, similarity_fun=similarity_fun)
        process_frame_data.filter_batch_fun = filter_fun

        output.append(process_frame_data)

    return output


def init_movie_paths(input_dir: Path, input_extension: str) -> list[Path]:
    glob_mask = input_dir / f"*{input_extension}"
    movies_paths = glob.glob(str(glob_mask))

    return [Path(i) for i in movies_paths]


def load_efficientnet():
    model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    return model, device


if __name__ == '__main__':
    main()
