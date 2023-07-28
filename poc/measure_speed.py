import csv
import time

import click
import numpy as np

import rectify
import cv2
import json

from speed import CarSpeedEstimator

show_scale = 0.6

frame_size = (1920, 1080)
motion_roi = (200, 300, 200, 100)  # 300:-100,500:-500 # motion_roi[1]:-motion_roi[3],motion_roi[0]:-motion_roi[2]
stitch_roi = (1100, 0, 400, 0)

# TODO zmienić na strukturę danych
start_point = (motion_roi[0], motion_roi[1])
end_point = (frame_size[0] - motion_roi[2], frame_size[1] - motion_roi[3])
color = (255, 0, 0)
thickness = 1


def save_to_csv_file(headers, measurements, output_csv):
    with open(output_csv, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for measurement in measurements:
            writer.writerow(measurement)


def display_frame(frame, cropped, dots):
    areas = np.zeros_like(frame)
    areas = cv2.rectangle(areas, start_point, end_point, color, thickness)
    frame = cv2.add(frame, areas)

    # Overlaying frame with dots window
    cropped = cv2.add(cropped, dots)
    frame[start_point[1]:end_point[1], start_point[0]:end_point[0], :] = cropped

    frame = cv2.resize(frame, (int(frame.shape[1] * show_scale), int(frame.shape[0] * show_scale)))
    cv2.imshow('result', frame)

    cv2.waitKey(1)


@click.command()
@click.argument("input_movie")
@click.argument("output_csv")
@click.option("--display", is_flag=True)
def main(input_movie, output_csv, display):
    input_cam = cv2.VideoCapture(input_movie)
    if not input_cam.isOpened():
        print("Error opening video stream or file")

    meter = CarSpeedEstimator()

    print(f"started {input_movie} processing")

    count = 0
    measurements = []  # TODO zmiana stuktury danych
    while input_cam.isOpened():
        ret, frame = input_cam.read()
        if ret:
            cropped_frame = frame[motion_roi[1]:-motion_roi[3], motion_roi[0]:-motion_roi[2]]
            dots = np.zeros_like(cropped_frame)
            velocity, dots = meter.next(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY), debug=dots)

            if display:
                display_frame(frame, cropped_frame, dots)

            x, y = velocity
            measurements.append((count, x, y))

            if count % 50 == 0:
                print(f"rendered: {count} frames")

            count = count + 1
        else:
            break

    input_cam.release()
    cv2.destroyAllWindows()

    headers = ["frame", 'x', 'y']
    save_to_csv_file(headers, measurements, output_csv)


if __name__ == '__main__':
    main()
