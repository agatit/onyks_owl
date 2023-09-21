import os
from dataclasses import astuple

import click

import cv2
import json
import numpy as np

from RegionOfInterest import RegionOfInterest
from stitch.rectify.FrameRectifier import FrameRectifier
from stitch.speed.CarSpeedEstimator import CarSpeedEstimator
from stitch.CarStitcherRoi import CarStitcherRoi
from stitch.speed.VelocityEstimator import VelocityEstimator

show_scale = 0.7

# frame_size = (1920, 1080)
# motion_roi = (200, 300, 200, 100)  # 300:-100,500:-500 # motion_roi[1]:-motion_roi[3],motion_roi[0]:-motion_roi[2]
# stitch_roi = (1100, 0, 400, 0)

# test = (0, 0, 500, 600)
# test_roi = RegionOfInterest.from_margin_px(frame_size, *(0, 0, 500, 600))
# motion_roi =

@click.command()
@click.argument("video_path")
@click.argument("config_json")
def main(video_path, config_json):
    pause = False
    path, filename = os.path.split(os.path.abspath(video_path))
    basename, extension = os.path.splitext(filename)

    with open(config_json) as f:
        config = json.load(f)

    frame_size = (1920, 1080)
    frame_rectifier = FrameRectifier(config, *frame_size)
    frame_rectifier.calc_maps()

    motion_roi = RegionOfInterest.from_margin_px(frame_size, *(40, 0, 100, 0))
    stitch_roi = RegionOfInterest.from_margin_px(frame_size, *(0, 0, 0, 1100))

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    meter = CarSpeedEstimator()
    velocity_estimator = VelocityEstimator()
    # stitcher = CarStitcherDelayed(roi_size=stich_roi, delay=50)

    roi_size = (1100, 0, 400, 0)
    stitcher = CarStitcherRoi(roi_size=roi_size)
    # deblur = Deblur(51)
    # deblur.set_speed(120, 0, 1, 1.2)

    frame_no = 0

    while cap.isOpened():

        frame_no = frame_no + 1

        ret, frame = cap.read()

        if ret:

            # prespektywa
            rectified = frame_rectifier.rectify(frame)
            # rectified = frame

            # usunięcie rozmycia
            # rectified = deblur.next(rectified)

            # crop
            cropped = motion_roi.crop_numpy_array(rectified)

            # pomiar prędkości
            debug = np.zeros_like(cropped)
            velocity, debug, _ = meter.next(cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY), debug=debug)
            velocity = velocity_estimator.get_velocity(cropped)
            print(velocity)
            velocity = astuple(velocity)
            # print(f"velocity={velocity}")
            cropped = cv2.add(cropped, debug)

            # sklejanie
            result = stitcher.next(rectified, velocity)

            # wyświetlanie :)
            if result is not None:
                areas = np.zeros_like(result)

                areas = cv2.rectangle(areas, motion_roi.p1, motion_roi.p2, (255, 0, 0), 1)
                areas = cv2.rectangle(areas, stitch_roi.p1, stitch_roi.p2, (0, 255, 0), 1)

                result = cv2.add(result, areas)
                result = cv2.resize(result, (int(result.shape[1] * show_scale), int(result.shape[0] * show_scale)))
                cv2.imshow('result', result)

            cropped = cv2.resize(cropped, (int(cropped.shape[1] * show_scale), int(cropped.shape[0] * show_scale)))
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


if __name__ == '__main__':
    main()
