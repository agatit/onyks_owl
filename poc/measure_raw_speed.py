import csv
import json
import os
from tqdm import tqdm
from dataclasses import dataclass
from datetime import datetime

import click
import cv2
import numpy as np

from io_utils.csv import CsvData, to_csv
from io_utils.utils import timestamp_output_file, get_current_time
from stitch.rectify.FrameRectifier import FrameRectifier
from stitch.speed.CarSpeedEstimator import CarSpeedEstimator
from stitch.RegionOfInterest import RegionOfInterest
from stitch.speed.VelocityEstimator import VelocityEstimator
from stitch.speed.VelocityFromFrames import VelocityFromFrames

show_scale = 0.6

frame_size = (1920, 1080)
motion_roi = RegionOfInterest.from_margin_px(frame_size, *(50, 100, 50, 200))
headers = ["frame", "x", "y"]
interrupt_program = False


def display_frame(frame, cropped, dots, delay):
    start_point = motion_roi.p1
    end_point = motion_roi.p2
    color = (0, 0, 255)
    thickness = 5

    areas = np.zeros_like(frame)
    areas = cv2.rectangle(areas, start_point, end_point, color, thickness)
    frame = cv2.add(frame, areas)

    # Overlaying frame with dots window
    cropped = cv2.add(cropped, dots)
    frame[start_point[1]:end_point[1], start_point[0]:end_point[0], :] = cropped

    frame = cv2.resize(frame, (int(frame.shape[1] * show_scale), int(frame.shape[0] * show_scale)))
    cv2.imshow('result', frame)

    key = cv2.waitKey(delay)

    if key & 0xFF == ord('q'):
        global interrupt_program
        interrupt_program = True


@click.command()
@click.argument("input_movie")
@click.argument("output_directory")
@click.argument("rectify_config")
@click.option("-d", "--display", "display", default=0, show_default=True)
def main(input_movie, rectify_config, output_directory, display):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")

    with open(rectify_config) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    meter = VelocityFromFrames()

    print(f"started {input_movie} processing")

    count = 0
    measurements = []

    total_frames = input_cam.get(cv2.CAP_PROP_FRAME_COUNT)

    with tqdm(total=total_frames) as pbar:
        while input_cam.isOpened():
            ret, frame = input_cam.read()
            if ret:
                frame = frame_rectifier.rectify(frame)
                cropped_frame = motion_roi.crop_numpy_array(frame)

                raw_velocities = meter.next(cropped_frame)

                if display > 0:
                    dots = meter.draw_point_from_last_record()
                    display_frame(frame, cropped_frame, dots, display)
                    if interrupt_program:
                        break

                for raw_velocity in raw_velocities:
                    measurements.append(tuple(raw_velocity))
            else:
                break

            count = count + 1
            pbar.update(1)

    input_cam.release()
    cv2.destroyAllWindows()

    file_name = timestamp_output_file("csv", get_current_time())
    output_file = os.path.join(output_directory, file_name)

    if not interrupt_program:
        with open(output_file, 'w') as file:
            csv_data = CsvData(headers, measurements)
            to_csv(file, csv_data)


if __name__ == '__main__':
    main()
