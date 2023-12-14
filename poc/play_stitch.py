import os

import click

import cv2
import json
import numpy as np

from display.RegionOfInterest import RegionOfInterest
from stitch.rectify.FrameRectifier import FrameRectifier
from stitch.CarStitcherRoi import CarStitcherRoi
from stitch.speed.VelocityEstimator import VelocityEstimator
from io_utils.csv import CsvData, to_csv
from stitch.speed.regression.FilterErrorMethod import FilterErrorMethod

show_scale = {
    "main": 0.5,
    "velocity": 0.7
}


@click.command()
@click.argument("video_path")
@click.argument("config_json")
@click.option("-exv", "--export_velocity", "export_velocity_path", help="export velocity to csv")
def main(video_path, config_json, export_velocity_path):
    pause = False
    path, filename = os.path.split(os.path.abspath(video_path))
    basename, extension = os.path.splitext(filename)

    with open(config_json) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    roi_size = (0, 640, 0, 1200)
    # roi_size = (0, 640, 0, 640)
    motion_roi = RegionOfInterest.from_margin_px(frame_size, *roi_size)
    stitch_roi = RegionOfInterest.from_margin_px(frame_size, *roi_size)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    # velocity_estimator = VelocityEstimator(LstsqMethod(), LstsqMethod())
    velocity_estimator = VelocityEstimator(FilterErrorMethod(True), FilterErrorMethod(True))
    # velocity_estimator = VelocityEstimator(OlsMethod(), OlsMethod())

    roi_size = (
        stitch_roi.margins["left"],
        stitch_roi.margins["top"],
        stitch_roi.margins["right"],
        stitch_roi.margins["bottom"]
    )
    # stitcher = CarStitcherDelayed(roi_size=stich_roi, delay=50)
    stitcher = CarStitcherRoi(roi_size=roi_size)
    # deblur = Deblur(51)
    # deblur.set_speed(120, 0, 1, 1.2)

    frame_no = 0
    velocity_data = []
    raw_velocity_data = []

    while cap.isOpened():

        frame_no = frame_no + 1

        ret, frame = cap.read()

        if ret:

            # prespektywa
            rectified = frame_rectifier.rectify(frame)

            # usunięcie rozmycia
            # rectified = deblur.next(rectified)

            # crop
            cropped = motion_roi.crop_numpy_array(rectified)

            # pomiar prędkości
            velocity = velocity_estimator.get_velocity(cropped)
            dots = velocity_estimator.velocity_from_frames.draw_point_from_last_record()
            print(velocity)
            # print(f"velocity={velocity}")
            cropped = cv2.add(cropped, dots)

            if export_velocity_path is not None:
                frame = velocity_estimator.frames_counter
                data = (frame, velocity[0], velocity[1])
                velocity_data.append(data)

            # sklejanie
            result = stitcher.next(rectified, velocity)

            # wyświetlanie :)
            if result is not None:
                areas = np.zeros_like(result)

                areas = cv2.rectangle(areas, motion_roi.p1, motion_roi.p2, (255, 0, 0), 1)
                areas = cv2.rectangle(areas, stitch_roi.p1, stitch_roi.p2, (0, 255, 0), 1)
                result = cv2.add(result, areas)

                scale = show_scale["main"]
                result = cv2.resize(result, (int(result.shape[1] * scale), int(result.shape[0] * scale)))
                cv2.imshow('result', result)

            scale = show_scale["velocity"]
            cropped = cv2.resize(cropped, (int(cropped.shape[1] * scale), int(cropped.shape[0] * scale)))
            cv2.imshow('cropped', cropped)

            if pause:
                c = cv2.waitKey(-1)
            else:
                c = cv2.waitKey(1)
            if c & 0xFF == ord('q'):
                break
            if c & 0xFF == ord('s'):
                cv2.imwrite(os.path.join(path, f"{basename}_{frame_no}.png"), rectified)
            elif c & 0xFF == ord(' '):
                pause = not pause

        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    headers = ["frame", "x", "y"]
    if export_velocity_path is not None:
        csv_data = CsvData(headers, velocity_data)

        with open(export_velocity_path, 'w') as file:
            to_csv(file, csv_data)


if __name__ == '__main__':
    main()
