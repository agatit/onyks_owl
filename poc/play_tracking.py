import json

import click
import cv2
import yaml

from display.utils import scale_image_by_percent
from stitch.rectify.FrameRectifier import FrameRectifier
from yolo.yolo_detectors.YoloDetectorV8 import YoloDetectorV8


@click.command()
@click.option("-in", "--input_movie", "input_movie",
              required=True, type=click.Path(exists=True),
              help="movie to track")
@click.option("-c", "--config", "config_path", type=click.Path(exists=True, file_okay=True),
              required=True, default="resources/find_frames_with_tags.yaml", help="yaml config path")
@click.option("-rc", "--rectify_config", "rectify_config_path", type=click.Path(exists=True, file_okay=True),
              help="rectify config path")
@click.option("-mp", "--model_path", "model_path", type=click.Path(exists=True, file_okay=True),
              required=True, help="yolov8 model path")
@click.option("-sc", "--scale", "scale", type=int,
              default=60, help="image scaling percentage factor")
def main(input_movie, config_path, rectify_config_path, model_path, scale):
    cap = cv2.VideoCapture(input_movie)

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    frame_rectifier = None
    if rectify_config_path:
        with open(rectify_config_path) as f:
            rectify_config = json.load(f)
        frame_size = config["image_size"]["width"], config["image_size"]["height"]
        frame_rectifier = FrameRectifier(rectify_config, *frame_size)
        frame_rectifier.calc_maps()

    model = YoloDetectorV8(model_path, verbose=False)

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:

            if frame_rectifier:
                frame = frame_rectifier.rectify(frame)

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)
            
            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            annotated_frame = scale_image_by_percent(annotated_frame, scale)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
