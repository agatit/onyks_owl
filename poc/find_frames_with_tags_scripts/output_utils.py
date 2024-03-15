from itertools import groupby
from pathlib import Path

from yolo.YoloDataset import YoloDataset
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


def filter_output_json(output_json, filter_config):
    for dataset_name, frames in output_json.items():
        last_label_occurrence = {label: 0 for label in filter_config["labels"]}
        step = filter_config["step"]
        confidence_threshold = filter_config["confidence_threshold"]

        def filter_output_json_wrapper(frame: dict):
            return filter_output_json_frames(frame, last_label_occurrence, step, confidence_threshold)

        output_json[dataset_name] = list(filter(filter_output_json_wrapper, frames))


def filter_output_json_frames(frame: dict, last_label_occurrence: dict, step: int, confidence_threshold: float):
    class_name = frame["detection_result"]["class_name"]
    confidence = frame["detection_result"]["confidence"]
    frame_number = frame["frame_number"]

    if class_name not in last_label_occurrence.keys():
        return False

    if confidence < confidence_threshold:
        return False

    last_occurrence = last_label_occurrence[class_name]
    current_occurrence = frame_number

    passed_frames_number = abs(last_occurrence - current_occurrence)
    if 0 < passed_frames_number < step:
        return False
    else:
        last_label_occurrence[class_name] = current_occurrence
        return True


def init_datasets_from_output_json(input_dir: Path, output_dir: Path, output_json: dict,
                                   image_extension: str = ".jpg") -> list[YoloDataset]:
    yolo_datasets = []
    for dataset_name, frames in output_json.items():
        dataset_path = input_dir / dataset_name

        yolo_dataset = YoloDataset(dataset_path, output_dir, image_extension=image_extension, dataset_name=dataset_name)

        for frame_number, grouped_frames in groupby(frames, lambda frame: frame["frame_number"]):
            yolo_formats = [YoloFormat(**i["detection_result"]["yolo_format"])
                            for i in grouped_frames if i["detection_result"]]

            image_name = str(frame_number) + image_extension
            image_path = dataset_path / image_name

            new_dataset_part = YoloDatasetPart(image_path, yolo_formats)
            yolo_dataset.yolo_dataset_parts.append(new_dataset_part)

        yolo_datasets.append(yolo_dataset)
    return yolo_datasets
