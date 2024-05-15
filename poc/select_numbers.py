import os
from dataclasses import field, dataclass
from pathlib import Path
from typing import Iterable, Iterator, Any

import tkinter as tk

import click
import yaml
from PIL import Image

from find_frames_with_tags_scripts.FindFramesWithTagsData import FindFramesWithTagsData
from find_frames_with_tags_scripts.output_json import load_output_json
from io_utils.utils import make_directories
from io_utils.yaml import Options, init_options
from ocr.datasets.Bbox import Bbox
from ocr.datasets.FullDatasetPart import FullDatasetPart
from selector.SelectorData import SelectorData
from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.gui.components.EntryWithLabel import EntryWithLabel
from selector.init_commands import init_default_commands, unbind_event
from selector.init_listeners import init_default_listeners
from selector.init_main_window import init_default_main_window
from selector.saving.Checkpoint import init_checkpoint
from selector.saving.SaveManager import SaveManager
from yolo.DetectionResult import DetectionResult


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              default=".", help="find_with_frames_tags.py output directory")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              default=".", help="output directory")
@click.option("-c", "--config", "config",
              required=True, type=click.Path(exists=True),
              default="select_frames_with_tags.yaml", help="path to config")
def main(input_dir, output_dir, config):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    make_directories(output_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    output_json = load_output_json(input_dir)
    output_json_gen = filter_output_json_gen(output_json, config, input_dir)

    checkpoints: Options = {
        "auto1": init_checkpoint,
        "auto2": init_checkpoint
    }
    checkpoints = init_options(checkpoints, config["checkpoints"])

    labels = config["names"]
    max_image_number = config["max_images"]

    for dataset_name, results in output_json_gen:
        save_manager = SaveManager(dataset_name)
        [save_manager.add_checkpoint(checkpoint) for checkpoint in checkpoints]

        detection_results_gen = (FindFramesWithTagsData(**i) for i in results)

        model = SelectNumbersModel(
            save_manager=save_manager,
            labels=labels,
            max_images=max_image_number,
            dataset_name=dataset_name,
            find_frames_with_tags_gen=detection_results_gen,
        )
        app = SelectNumbers(model)

        try:
            app.notify_listener("load_checkpoint")
        except FileNotFoundError:
            print(f"Not found: {model.save_manager.get_latest_checkpoint()}")

        if model.to_export:
            app.destroy()
            continue

        app.mainloop()

        if not model.to_export:
            break

        # full_dataset_parts = model.export_gen()
        #
        # # labels_json_path = output_dir / "labels.json"
        # movie_result_dir = output_dir / dataset_name
        #
        # labels_json_path = movie_result_dir / "labels.json"
        # images_path = movie_result_dir / "images"

        # with open(output_path, "w") as file:
        #     json.dump(rectify_config, file)

        # dataset.yolo_dataset_parts = new_parts
        # dataset.export()

        del app


def filter_output_json_gen(output_json: dict, config: dict, input_dir: Path):
    dirs = os.listdir(input_dir)
    output_json = {k: v for k, v in output_json.items() if k in dirs}

    selected_labels = config["names"].keys()

    for dataset_name, results in output_json.items():
        selected_results = []

        for result in results:
            detection_result = result["detection_result"]

            if detection_result is not None and check_detection_result_id(detection_result, selected_labels):
                selected_results.append(result)

        yield dataset_name, selected_results


def check_detection_result_id(detection_result: dict, enabled_id: Iterable) -> bool:
    return detection_result["yolo_format"]["class_id"] in enabled_id


@dataclass(kw_only=True)
class SelectNumbersData(SelectorData):
    dataset_part: FullDatasetPart

    track_id: int = -1
    proposed_text: str = ""


@dataclass(kw_only=True)
class SelectNumbersModel(SelectorModel):
    dataset_name: str

    find_frames_with_tags_gen: Iterator[FindFramesWithTagsData]
    _data: list[SelectNumbersData] = field(init=False, default_factory=list)

    def __post_init__(self):
        super().__post_init__()

    def _init_selector_data(self) -> None:
        dataset_name = self.dataset_name
        max_entities = self.max_images

        select_number_data = []
        for index, find_frame_with_tags_data in enumerate(self.find_frames_with_tags_gen):
            if max_entities > 0 and index < max_entities:
                break

            detection_result_dict = find_frame_with_tags_data.detection_result
            detection_result = DetectionResult(**detection_result_dict)

            src_file_name = find_frame_with_tags_data.file_name
            src_file_path = Path(dataset_name) / src_file_name

            with Image.open(src_file_path) as image:
                width, height = image.size

            full_dataset_part = FullDatasetPart(
                src_file_name=src_file_name,
                src_file_width=width,
                src_file_height=height,
                bbox=Bbox.from_xyxy(**detection_result.bounding_box),
                reg_text="",
                label_id=detection_result.yolo_format["class_id"]
            )

            new_select_number_data = SelectNumbersData(
                image_path=src_file_path,
                dataset_part=full_dataset_part,
                track_id=detection_result.track_id,
                proposed_text=""
            )

            select_number_data.append(new_select_number_data)

        self._selector_data = select_number_data

    def save_checkpoint(self, checkpoint_name: str, current_index: int):
        checkpoint_data = (self.to_export, current_index, self._data)
        checkpoint = self.save_manager.get_checkpoint(checkpoint_name)
        checkpoint.save(checkpoint_data)

    def export_gen(self) -> Iterable[FullDatasetPart]:
        for data in self._data:
            yield data.dataset_part


class SelectNumbers(Selector):
    def __init__(self, model: SelectNumbersData, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def _init_variables(self):
        super()._init_variables()

        scale_str = "!mainwindow.sidebar.!scalewithlabel"
        self.var_register.add_var("brightness_var", self.nametowidget(scale_str).scale_var)

        entry_str = "!mainwindow.image_canvas_container.entry_number"
        self.var_register.add_var("number_var", self.nametowidget(entry_str).entry_var)

    def _init_main_window(self):
        model = self.model
        main_window = self.main_window

        init_default_main_window(self, model)

        image_canvas_container_str = "!mainwindow.image_canvas_container"
        image_canvas_container = self.nametowidget(image_canvas_container_str)

        entry_with_label = EntryWithLabel(image_canvas_container, name="entry_number", label_text="Number:")
        entry_with_label.entry.config(font="Calibri 18")
        entry_with_label.pack(fill=tk.BOTH, pady=5)

    def _init_commands(self):
        init_default_commands(self, self.model)

        unbind_event(self, "<KeyRelease-w>")
        unbind_event(self, "<KeyRelease-s>")
        unbind_event(self, "<KeyRelease-a>")
        unbind_event(self, "<KeyRelease-d>")


    def _init_listeners(self):
        init_default_listeners(self, self.model)

    def _init_canvas_callbacks(self):
        pass


if __name__ == '__main__':
    main()
