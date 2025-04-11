from pathlib import Path

import click
import cv2
import yaml
from pydantic import BaseModel, Field

from display.draw import put_text_on_image_margin
from io_utils.utils import make_clean_dir


class MetricConfig(BaseModel):
    name: str
    kwargs: dict = Field(default_factory=dict)


class Params(BaseModel):
    model: dict = Field(default_factory=dict)
    inference: dict = Field(default_factory=dict)


class ApplicationConfig(BaseModel):
    input_image_extension: str


class Config(BaseModel):
    application: ApplicationConfig
    basic_params: Params
    measurements_params: Params

    context_metrics: list[MetricConfig] = Field(default_factory=list)
    str_metrics: list[MetricConfig] = Field(default_factory=list)


# metrics


@click.command()
@click.option("-in", "--input", "input_dir",
              required=True, type=click.Path(exists=True, dir_okay=True),
              help="select directory with movies_paths")
@click.option("-out", "--output", "output_dir",
              required=True, type=click.Path(),
              help="select output directory for measurements")
@click.option("-c", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/evaluate_ocr.yaml", help="yaml config path")
def main(input_dir, output_dir, config_path):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = Config(**config)

    pass
    # make_clean_dir(output_dir)

    # img_path_0 = Path('vertical_0.jpg')
    # img = cv2.imread(str(img_path_0))
    #
    # result = put_text_on_image_margin(img, ["test", "aaaaaaa1233525", "abc"])
    # # result = add_text_to_image(img, "test")
    # cv2.imwrite('vertical_0_r.jpg', result)


if __name__ == '__main__':
    main()

# class BoundingBox(BaseModel):
#     top_left: tuple[int, int]
#     top_right: tuple[int, int]
#     bottom_right: tuple[int, int]
#     bottom_left: tuple[int, int]
#
#
# class Prediction(BaseModel):
#     text: str
#     confidence: float
#
#
# class OCRResult(BaseModel):
#     bbox: BoundingBox
#     prediction: Prediction
#
#
# def ocr_results_from_raw_ocr(raw_ocr: list) -> list[OCRResult]:
#     ocr_results = []
#
#     for ocr_result in raw_ocr:
#         bbox = BoundingBox(
#             top_left=ocr_result[0][0],
#             top_right=ocr_result[0][1],
#             bottom_right=ocr_result[0][2],
#             bottom_left=ocr_result[0][3]
#         )
#         prediction = Prediction(
#             text=ocr_result[1][0],
#             confidence=ocr_result[1][1]
#         )
#         ocr_results.append(
#             OCRResult(
#                 bbox=bbox,
#                 prediction=prediction
#             )
#         )
#
#     return ocr_results
