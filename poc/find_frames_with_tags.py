import copy
import dataclasses
import glob
import json
import os
import shutil
from pathlib import Path

import click
import cv2
import yaml
from tqdm import tqdm

from find_frames_with_tags_scripts.OutputData import OutputData
from find_frames_with_tags_scripts.ProcessData import ProcessData
from opencv_tools.image_transformations import draw_image_with_rectangles
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.YoloDetector import YoloDetector

BOUNDING_BOX_FILE_SUFFIX = "_b"


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
    print(f"{__file__} started")
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    rectify_config = {}
    if rectify_config_path:
        with open(rectify_config_path) as f:
            rectify_config = json.load(f)

    # check if output_dir is empty
    output_dir = Path(output_dir)
    if not output_dir.is_dir():
        os.mkdir(output_dir)

    if len(list(output_dir.iterdir())) > 0:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)

    input_extension = config["extension"]["input"]
    glob_mask = Path(input_dir) / f"*.{input_extension}"
    movies_paths = glob.glob(str(glob_mask))
    movies_paths = [Path(i) for i in movies_paths]

    confidence_threshold = float(config["model"]["confidence_threshold"])
    detector = YoloDetector(model_path, confidence_threshold)
    detector.enable_multiprocessing()

    process_data = []
    for movie_path in movies_paths:
        frame_rectifier = None
        if len(rectify_config) > 0:
            frame_rectifier = init_rectifier(rectify_config)

        _output_dir = output_dir / movie_path.stem
        os.mkdir(_output_dir)

        output_extension = config["extension"]["output"]
        labels_copy = copy.copy(config["labels"])

        data = ProcessData(movie_path, _output_dir, output_extension, frame_rectifier, detector, labels_copy)
        process_data.append(data)

    for data in process_data:
        input_cam = cv2.VideoCapture(str(data.movie_path))
        frame_count = int(input_cam.get(cv2.CAP_PROP_FRAME_COUNT))
        input_cam.release()

        for _ in tqdm(process_gen(data), desc=data.movie_path.name, total=frame_count):
            pass

    outputs = {}
    for data in process_data:
        movie_name = data.movie_path.stem
        output_data = [dataclasses.asdict(i) for i in data.output_data]
        outputs[movie_name] = output_data

    # if filter_config:
    #     with open(filter_config) as f:
    #         filter_config = yaml.load(f, Loader=yaml.FullLoader)
    #
    #     filter_output_json(output_json, filter_config)

    output_file = output_dir / "output.json"
    with open(str(output_file), 'w') as file:
        json.dump(outputs, file)


def init_rectifier(rectify_config: dict, frame_size: tuple[int, int] = (1920, 1080)) -> FrameRectifier:
    frame_rectifier = FrameRectifier(rectify_config, *frame_size)
    frame_rectifier.calc_maps()

    return frame_rectifier


def process_gen(process_data: ProcessData) -> None:
    input_cam = cv2.VideoCapture(str(process_data.movie_path))

    extension = process_data.output_extension
    output_extension = f".{extension}"

    counter = 0
    while input_cam.isOpened():
        result, frame = input_cam.read()
        if result:

            if process_data.rectifier:
                frame = process_data.rectifier.rectify(frame)

            detection_results = process_data.model.detect_image(frame, process_data.labels)

            if len(detection_results) > 0:
                for index, detection_result in enumerate(detection_results):
                    name = detection_result.class_name
                    file_name = f"{counter}_{name}_{index}" + output_extension
                    file_path = process_data.output_dir / file_name

                    output_data = OutputData(counter, file_name, detection_result)
                    process_data.output_data.append(output_data)

                    box = detection_result.bounding_box
                    cropped = frame[box.y1:box.y2, box.x1:box.x2]

                    cv2.imwrite(str(file_path), cropped)

                # save image
                frame_file_name = str(counter) + output_extension
                frame_file_path = str(process_data.output_dir / frame_file_name)

                cv2.imwrite(frame_file_path, frame)

                # save image with drawn bounding boxes
                frame_file_name = str(counter) + BOUNDING_BOX_FILE_SUFFIX + output_extension
                frame_file_path = str(process_data.output_dir / frame_file_name)
                for detection_result in detection_results:
                    frame = detection_result.draw_on_image(frame)

                cv2.imwrite(frame_file_path, frame)

            counter += 1
            yield
        else:
            break

    input_cam.release()


if __name__ == '__main__':
    main()
