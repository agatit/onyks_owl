# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł poddający strumien video pod transformację perspektywy"""

# Module imports
import sys
import time
import stream_video
import stream_data
import module_base

# Perspective transform imports
import pickle
import cv2
import numpy as np
from os.path import join, basename
import scipy.spatial.distance
import math

# Program local libraries
from perspective.camera_calibration import calibrate_camera_and_pickle_mtx_dist
from perspective.load_parameters import load_camera_mtx_dist_from_json as load_mtx_dist
from perspective.perspective_transform import get_perspective_Mtx_with_aspect_ratio


class Module(module_base.Module):
    def streams_init(self):
        self.input_classes = {
            "color": stream_video.Consumer,
            "metrics": stream_data.Consumer
        }
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }                

    def task_process(self, input_task_data, input_stream):
        """przetwarzanie strumieni"""

        # trapezoid_coords = self.params.get('trapezoid_coords')
        trapezoid_coords = self.params.get('trapezoid_coords_WISENET_t1')
        # print(trapezoid_coords)

        """get parameters for Wisenet camera calibration"""
        calibrate_camera_and_pickle_mtx_dist()
        mtx, dist = load_mtx_dist()

        with self.task_emit({}) as output_stream:
            runonce_flag = 0
            for input_data in input_stream:
                begin = time.time()

                if runonce_flag == 0:
                    M, W, H = get_perspective_Mtx_with_aspect_ratio(input_data['color'], trapezoid_coords)
                    print('Mtx, W, H')
                    runonce_flag = 1
                """undistort"""
                undist_frame = cv2.undistort(input_data['color'], mtx, dist, None, mtx)
                # in_transformed = cv2.warpPerspective(input_data['color'], M, (W, H))
                in_transformed = cv2.warpPerspective(undist_frame, M, (W, H))
                print(f"czas wykonania: {time.time()-begin} s")

                output_data = {
                    "color": in_transformed,
                    "metrics": input_data["metrics"]
                }

                output_stream.emit(output_data)


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
