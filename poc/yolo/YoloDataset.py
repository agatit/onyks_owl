import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from yolo.YoloDatasetPart import YoloDatasetPart


@dataclass
class YoloDataset:
    IMAGE_DIR_NAME: ClassVar[str] = "images"
    LABEL_DIR_NAME: ClassVar[str] = "labels"

    input_dir: Path
    output_dir: Path

    image_extension: str = ".jpg"
    labels_extension: str = ".txt"
    yolo_dataset_parts: list[YoloDatasetPart] = field(default_factory=list)

    output_images_dir: Path = field(init=False)
    output_labels_dir: Path = field(init=False)

    def __post_init__(self):
        self.output_images_dir = self.output_dir / self.IMAGE_DIR_NAME
        self.output_labels_dir = self.output_dir / self.LABEL_DIR_NAME

    def export(self) -> None:
        for dataset_part in self.yolo_dataset_parts:
            output_image_name = dataset_part.output_file_name + self.image_extension
            output_image_path = self.output_images_dir / output_image_name

            shutil.copyfile(dataset_part.original_image_path, output_image_path)

            output_label_name = dataset_part.output_file_name + self.labels_extension
            output_label_path = self.output_labels_dir / output_label_name

            str_yolo_formats = [i.to_yolo_txt_line() for i in dataset_part.yolo_formats]

            with open(output_label_path, "w") as file:
                file.writelines(str_yolo_formats)

    def split(self) -> None:
        pass
