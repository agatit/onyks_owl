import os
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

import tkinter as tk
import click
import yaml
from PIL import Image

from find_frames_with_tags_scripts.output_json import load_output_json
from find_frames_with_tags_scripts.output_utils import init_datasets_from_output_json
from io_utils.utils import make_directories
from io_utils.yaml import Options, init_options
from selector.SelectorData import SelectorData
from selector.Selector import Selector
from selector.SelectorModel import SelectorModel
from selector.canvas_callbacks.draw.DrawLabelRectangles import draw_label_rectangles
from selector.canvas_callbacks.transform.Resize import resize
from selector.commands.listbox.ChangeLabelToSelectedCommand import ChangeLabelToSelectedCommand
from selector.commands.listbox.GlowSelectedLabelCommand import GlowSelectedLabelCommand
from selector.commands.listbox.RemoveLabelCommand import RemoveLabelCommand
from selector.commands.listbox.SelectLabelCommand import SelectLabelCommand
from selector.gui.LabelRectangle import LabelRectangle
from selector.gui.components.ImageCanvas import ImageCanvas
from selector.gui.components.ScrollableListbox import ScrollableListbox
from selector.init_commands import init_default_commands, register_command
from selector.init_listeners import init_default_listeners, reload_main_window
from selector.init_main_window import init_default_main_window
from selector.listeners.ReloadCounter import reload_counter
from selector.listeners.ReloadImage import reload_image
from selector.listeners.ReloadImageName import reload_image_name
from selector.listeners.ReloadLabel import reload_label
from selector.listeners.ReloadResultsListbox import reload_results_listbox
from selector.listeners.UpdateLabelText import update_label_text
from selector.saving.Checkpoint import init_checkpoint
from selector.saving.SaveManager import SaveManager
from selector.tracing.TraceRegister import trace_add
from yolo.YoloDataset import YoloDataset
from yolo.YoloDatasetPart import YoloDatasetPart
from yolo.YoloFormat import YoloFormat


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
@click.option("-qe", "--quick_export", "quick_export",
              type=int, default=-1,
              help="quick export mode, select number images to export")
@click.option("-li", "--last_image", "last_image",
              is_flag=True,
              help="last image mode, select number images to export")
def main(input_dir, output_dir, config, quick_export, last_image):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    images_dir = output_dir / "images"
    labels_dir = output_dir / "labels"
    make_directories(output_dir, images_dir, labels_dir)

    with open(config, encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    output_json = load_output_json(input_dir)

    # todo: wczytywanie z pliku konfiguracyjnego
    checkpoints: Options = {
        "auto1": init_checkpoint,
        "auto2": init_checkpoint
    }
    checkpoints = init_options(checkpoints, config["checkpoints"])

    dirs = os.listdir(input_dir)
    output_json = {k: v for k, v in output_json.items() if k in dirs}

    image_extension = config["image_extension"]
    yolo_datasets = init_datasets_from_output_json(input_dir, output_dir, output_json, image_extension)

    labels = config["names"]
    max_image_number = config["max_images"]

    for dataset in yolo_datasets:
        save_manager = SaveManager(dataset.dataset_name)
        [save_manager.add_checkpoint(checkpoint) for checkpoint in checkpoints]

        model = SelectFramesWithTagsModel(
            dataset=dataset,
            save_manager=save_manager,
            labels=labels,
            max_images=max_image_number
        )
        app = SelectFramesWithTags(model)

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

        new_parts = model.export_dataset_parts()
        dataset.yolo_dataset_parts = new_parts
        dataset.export()

        del app


@dataclass(kw_only=True)
class SelectFramesWithTagsModel(SelectorModel):
    dataset: YoloDataset

    def __post_init__(self):
        super().__post_init__()
        self._load_yolo_dataset_parts()

    def _init_selector_data(self) -> None:
        images = [i.original_image_path for i in self.dataset.yolo_dataset_parts]

        if self.max_images < 0:
            images_to_load = len(images)
        else:
            images_to_load = self.max_images

        self._selector_data = [SelectorData(image_path=image) for image in images[:images_to_load]]

    def save_checkpoint(self, checkpoint_name: str, current_index: int):
        checkpoint_data = (self.to_export, current_index, self._selector_data)
        checkpoint = self.save_manager.get_checkpoint(checkpoint_name)
        checkpoint.save(checkpoint_data)

    # @open_loading_screen
    def _load_yolo_dataset_parts(self):
        max_images = self.get_selector_data_len()
        labels = self.labels

        for process_data, dataset_part, in zip(self._selector_data[:max_images],
                                               self.dataset.yolo_dataset_parts[:max_images]):
            formats = dataset_part.yolo_formats

            label_rectangles = []
            for _format in formats:
                width, height = Image.open(dataset_part.original_image_path).size

                bounding_box = _format.to_bounding_box(width, height)

                label_rectangle = LabelRectangle(
                    label_id=_format.class_id,
                    label_text=labels[_format.class_id],
                    bounding_box=bounding_box
                )
                label_rectangles.append(label_rectangle)

            process_data.label_rectangles = label_rectangles

    def export_dataset_parts(self) -> list[YoloDatasetPart]:
        filtered = filter(lambda x: len(x.label_rectangles) > 0, self._selector_data)

        dataset_parts = []
        for process_data in filtered:
            image_path = process_data.image_path
            yolo_formats = self._process_data_to_yolo_formats(process_data)

            dataset_part = YoloDatasetPart(image_path, yolo_formats)
            dataset_parts.append(dataset_part)

        return dataset_parts

    @staticmethod
    def _process_data_to_yolo_formats(process_data):
        image_path = process_data.image_path

        yolo_formats = []
        for label_rectangle in process_data.label_rectangles:
            class_id = label_rectangle.label_id
            bounding_box = label_rectangle.bounding_box
            width, height = Image.open(image_path).size

            yolo_format = YoloFormat.from_bounding_box(class_id, width, height, bounding_box)
            yolo_formats.append(yolo_format)

        return yolo_formats


class SelectFramesWithTags(Selector):
    def __init__(self, model: SelectFramesWithTagsModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

        self.notify_listener("reload_main_window")

    def _init_variables(self):
        super()._init_variables()

        scale_str = "!mainwindow.sidebar.!scalewithlabel"
        scale = self.nametowidget(scale_str)
        self.var_register.add_var("brightness_var", scale.scale_var)

    def _init_main_window(self):
        model = self.model

        init_default_main_window(self, model)

        side_bar = self.nametowidget("!mainwindow.sidebar")

        classes_listbox = ScrollableListbox(side_bar, "Classes", name="class_listbox")
        classes_listbox.listbox.config(selectmode='browse')
        classes_listbox.pack(side=tk.TOP, expand=True, anchor=tk.N, fill=tk.BOTH)
        classes_listbox.listbox_var.set(list(model.labels.values()))

        results_listbox = ScrollableListbox(side_bar, "Results", name="results_listbox")
        results_listbox.listbox.config(selectmode='extended')
        results_listbox.pack(side=tk.TOP, expand=True, anchor=tk.S, fill=tk.BOTH)

        remove_button = tk.Button(results_listbox, text="Remove", name="remove_button")
        remove_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        change_results_button = tk.Button(results_listbox, text="Change", name="change_button")
        change_results_button.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def _init_commands(self):
        init_default_commands(self, self.model)

        defaults_args = self, self.model

        classes_listbox = self.nametowidget("!mainwindow.sidebar.class_listbox.listbox_container.!listbox")
        results_listbox = self.nametowidget("!mainwindow.sidebar.results_listbox.listbox_container.!listbox")
        remove_button = self.nametowidget("!mainwindow.sidebar.results_listbox.remove_button")
        change_button = self.nametowidget("!mainwindow.sidebar.results_listbox.change_button")

        register_partial = partial(
            register_command,
            app=self,
            target=self,
            mode_name="default",
            args=defaults_args,
            history_flag=True,
        )

        # list boxes
        key = "<<ListboxSelect>>"
        command = SelectLabelCommand
        args = defaults_args + (classes_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=False,
                         target=classes_listbox)

        key = "<<ListboxSelect>>"
        command = GlowSelectedLabelCommand
        args = defaults_args + (results_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=False,
                         target=results_listbox)

        key = "<KeyRelease-Delete>"
        command = RemoveLabelCommand
        args = defaults_args + (results_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=True,
                         target=results_listbox)

        key = "<Button-1>"
        command = RemoveLabelCommand
        args = defaults_args + (results_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=True,
                         target=remove_button)

        key = "<Button-1>"
        command = ChangeLabelToSelectedCommand
        args = defaults_args + (results_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=True,
                         target=change_button)

        key = "<KeyRelease-Return>"
        command = ChangeLabelToSelectedCommand
        args = defaults_args + (results_listbox,)
        register_partial(key=key, command=command, args=args, history_flag=True,
                         target=results_listbox)

    def _init_listeners(self):
        model = self.model
        init_default_listeners(self, model)

        mainwindow_str = "!mainwindow"
        topbar_str = "!mainwindow.!topbar"
        results_listbox_str = "!mainwindow.sidebar.results_listbox"
        image_canvas_str = "!mainwindow.!imagecanvas"

        index_var = "current_index_var"

        trace_add(
            register=self.var_register,
            var_name=index_var,
            mode="write",
            trace_name="reload_results_listbox",
            callback=partial(reload_results_listbox, self, model, results_listbox_str)
        )

        reload_main_window_callbacks: list = [
            partial(reload_image, self, model, image_canvas_str),
            partial(reload_image_name, self, model, topbar_str),
            partial(reload_counter, self, model, topbar_str),
            partial(reload_label, self, model, topbar_str),
            partial(update_label_text, self, model, None),
            partial(reload_results_listbox, self, model, results_listbox_str)
        ]

        self.add_listener("reload_main_window", partial(reload_main_window, *reload_main_window_callbacks))
        self.add_listener("reload_results_listbox", partial(reload_results_listbox, self, model, results_listbox_str))

    def _init_canvas_callbacks(self):
        model = self.model
        image_canvas: ImageCanvas = self.nametowidget("!mainwindow.!imagecanvas")

        image_canvas.image_transformations["resize"] = partial(resize, self, model, image_canvas)

        image_canvas.draw_callbacks["label_rectangles"] = partial(draw_label_rectangles, self, model, image_canvas)


if __name__ == '__main__':
    main()
