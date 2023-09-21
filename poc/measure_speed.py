import csv
from dataclasses import dataclass

import click
import cv2
import numpy as np

from stitch.speed.CarSpeedEstimator import CarSpeedEstimator
from stitch.RegionOfInterest import RegionOfInterest

show_scale = 0.6

frame_size = (1920, 1080)
motion_roi = RegionOfInterest.from_margin_px(frame_size, *(50, 100, 200, 200))  # motion_roi[1]:-motion_roi[3],motion_roi[0]:-motion_roi[2]


@dataclass
class Measurement:
    frame: int
    velocity: np.ndarray


def save_to_csv(file, headers, measurements):
    writer = csv.writer(file)

    writer.writerow(headers)
    for measurement in measurements:
        for velocity in measurement.velocity:
            data_to_store = (measurement.frame,) + tuple(velocity)
            writer.writerow(data_to_store)


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

    cv2.waitKey(delay)


@click.command()
@click.argument("input_movie")
@click.argument("output_file")
@click.option("-d", "--display", "display", default=0, show_default=True)
def main(input_movie, output_file, display):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")

    meter = CarSpeedEstimator()

    print(f"started {input_movie} processing")

    count = 0
    headers = ["frame", "x", "y", "status"]
    measurements = []

    while input_cam.isOpened():
        ret, frame = input_cam.read()
        if ret:
            cropped_frame = motion_roi.crop_numpy_array(frame)
            dots = np.zeros_like(cropped_frame)
            avg_velocity, dots, raw_velocity = meter.next(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY), debug=dots)

            if display > 0:
                display_frame(frame, cropped_frame, dots, display)

            measurements.append(Measurement(count, raw_velocity))

            if count % 50 == 0:
                print(f"rendered: {count} frames")

            count = count + 1
        else:
            break

    input_cam.release()
    cv2.destroyAllWindows()

    with open(output_file, 'w') as file:
        save_to_csv(file, headers, measurements)


if __name__ == '__main__':
    main()
