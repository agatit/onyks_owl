from pathlib import Path

import click
import cv2
from ultralytics import YOLO


@click.command()
@click.option("-in", "--input", "input_source",
              required=True, type=click.Path(exists=True, file_okay=True),
              help="path to source - https://docs.ultralytics.com/modes/predict/#inference-sources")
@click.option("-mp", "--model_path", "model_path",
              required=True, type=click.Path(exists=True, file_okay=True),
              help=".pt file")
def main(input_source, model_path):
    input_source = Path(input_source)
    input_dir = input_source.parent
    input_name = input_source.stem
    input_extension = input_source.suffix

    model = YOLO(model_path)
    results = model.track(input_source, persist=True)
    annotated_frame = results[0].plot()

    output_path = str(input_dir / f"{input_name}_b{input_extension}")

    cv2.imwrite(str(output_path), annotated_frame)

    # cv2.imshow("YOLOv8 Tracking", annotated_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
