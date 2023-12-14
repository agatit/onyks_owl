import copy
import os
import time
from itertools import chain

import click
import numpy as np

from io_utils.csv import CsvData, ndarray_to_list_tuple, to_csv
from speed_analyse_scripts.config_inits import init_movie_paths, init_rectifier, init_velocity_rois, \
    init_raw_velocities, init_measurements
import yaml

from display.RegionOfInterest import RegionOfInterest
from stitch.speed.VelocityEstimator import VelocityEstimator
from stitch.speed.regression.FilterErrorMethod import FilterErrorMethod
from stitch.speed.regression.LstsqMethod import LstsqMethod
import cv2
from tqdm import tqdm

from stitch.velocity_stream import open_video_capture

global config


def counter(_id, sleep_time):
    start = time.time()
    time.sleep(sleep_time)
    stop = time.time() - start
    print(f"{_id}: {stop}")


def display_rois(frame: np.ndarray, rois: list[RegionOfInterest], names: list[str], scaling: int):
    draw_frame = copy.deepcopy(frame)
    scaling = scaling / 100

    for roi, name in zip(rois, names):
        color = tuple(np.random.randint(0, 255, 3))
        color = [int(i) for i in color]
        draw_frame = cv2.rectangle(draw_frame, roi.p1, roi.p2, color, 3)

        padding = 50
        text_params = {
            "img": draw_frame,
            "text": name,
            "org": (roi.x1 + padding, roi.y1 + padding),
            "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
            "fontScale": 1,
            "color": color,
            "thickness": 2,
        }
        draw_frame = cv2.putText(**text_params)

    draw_frame = cv2.resize(draw_frame, (int(draw_frame.shape[1] * scaling), int(draw_frame.shape[0] * scaling)))
    cv2.imshow('ROIs', draw_frame)

    cv2.waitKey(-1)
    cv2.destroyAllWindows()


@click.command()
@click.option("-sc'", "--speed_config", "speed_config_path", default="resources/speed_analyse.yaml", required=True,
              help="yaml configuration for tests")
@click.option("-out", "--output", "output", default="resources/speed_analyse", required=True,
              help="directory with csv result file")
@click.option("-d", "--display", "display", default=-1,
              help="display first frame with ROIs with given % scaling")
def main(speed_config_path, output, display):
    global config

    with open(speed_config_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    frame_rectifier = init_rectifier(config)
    movie_paths = init_movie_paths(config)
    velocity_rois = init_velocity_rois(config)

    raw_velocities = init_raw_velocities(movie_paths, velocity_rois)

    # todo: do pliku
    velocity_estimators = {
        "lstsq": VelocityEstimator(LstsqMethod(), LstsqMethod()),
        # "OLS": VelocityEstimator(OlsMethod(), OlsMethod()),
        # "WLS": VelocityEstimator(WlsMethod(), WlsMethod()),
        # "Mean": VelocityEstimator(MeanMethod(), MeanMethod(), center=False),
        # "Median": VelocityEstimator(MedianMethod(), MedianMethod(), center=False),
        "Filter": VelocityEstimator(FilterErrorMethod(False), FilterErrorMethod(False), center=False),
        # "Filter_R": VelocityEstimator(FilterErrorMethod(True), FilterErrorMethod(True), center=False),
    }

    measurements = init_measurements(movie_paths, velocity_estimators, raw_velocities)

    print("Movie paths:")
    [print(f"\t{key}: {value}") for key, value in movie_paths.items()]
    print("Measurements:")
    [print(f"\t{measurement}") for measurement in measurements]

    min_frames = config["frames_range"]["min"]
    max_frames = config["frames_range"]["max"]
    for dataset_name, file_path in movie_paths.items():
        current_dataset_measurements = [i for i in measurements if i.dataset_name == dataset_name]

        with open_video_capture(file_path) as video_capture:
            total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

            counter = 0
            with tqdm(total=total_frames, desc=dataset_name) as pbar:
                while video_capture.isOpened():
                    ret, frame = video_capture.read()

                    if display > 0 and counter < 1:
                        frame = frame_rectifier.rectify(frame)

                        rois = [i.roi for i in raw_velocities if i.dataset_name == dataset_name]
                        names = [i.roi_name for i in raw_velocities if i.dataset_name == dataset_name]
                        display_rois(frame, rois, names, display)

                    if min_frames > 0 and counter < min_frames:
                        counter += 1
                        pbar.update(1)
                        continue

                    if max_frames > 0 and counter > max_frames:
                        pbar.update(total_frames - counter)
                        pbar.close()
                        break

                    if ret:
                        frame = frame_rectifier.rectify(frame)

                        for raw_velocity in raw_velocities:
                            cropped = raw_velocity.roi.crop_numpy_array(frame)
                            raw_velocity.append_velocity(cropped)

                            roi_name = raw_velocity.roi_name
                            current_roi_measurements = (i for i in current_dataset_measurements if
                                                        i.roi_name == roi_name)

                            for measurement in current_roi_measurements:
                                # measurement.timer.start()
                                velocity = measurement.velocity_estimator.get_velocity(cropped)
                                # measurement.timer.stop()

                                result = (counter, velocity[0], velocity[1])
                                measurement.results.append(result)
                    else:
                        break

                    counter += 1
                    pbar.update(1)

    # print(measurements[0].results)

    # todo: do osobnej funkcji
    # todo: dodać try i except
    headers = config["output_headers"]
    for movie in config["movies"]["movie"]:
        movie_name = movie["name"]
        output_dir = movie["output"]

        if os.path.exists(output_dir):
            os.rmdir(output_dir)
        os.mkdir(output_dir)


        # (results, prefix, roi)
        current_raw_velocities = ((ndarray_to_list_tuple(i.results), "raw", i.roi_name) for i in raw_velocities if
                                  i.dataset_name == movie_name)
        current_measurements = ((i.results, i.method_name, i.roi_name) for i in measurements if
                                i.dataset_name == movie_name)
        output_data = chain(current_raw_velocities, current_measurements)

        for results, prefix, roi in output_data:
            file_name = f"{prefix}_{roi}.csv"
            output_file_path = os.path.join(output_dir, file_name)

            csv_data = CsvData(headers, results)
            with open(output_file_path, "w") as file:
                to_csv(file, csv_data)

    # with Pool(5) as p:
    #     map_list = []
    #     for i in range(10):
    #         sleep_time = random.randint(1, 5)
    #         map_list.append((i, sleep_time))
    #     p.starmap(counter, map_list)


if __name__ == '__main__':
    main()
