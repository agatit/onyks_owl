# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł poddający strumien video pod transformację perspektywy"""

# Module imports
import sys
import time

import numpy as np

from pathlib import Path

if __package__ == '':
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[1]

    sys.path.append(str(parent))
    __package__ = 'onyks_owl' # TODO do pomyślenia czy ja tego potrzebuję...

import stream_video
import stream_data
import module_base
import cv2

# Program local libraries
from perspective.perspective_transform import get_perspective


class Module(module_base.Module):
    def __init__(self, argv):
        super(Module, self).__init__(argv)
        self.default_config['params'][1]['mtx'] = ['list', [[1161.107086941478,0.0,948.2004474733628],[0.0,1166.8887234211986,608.8830018574113],[0.0,0.0,1.0]]]
        self.default_config['params'][1]['dist'] = ['list', [[-0.5435658832121913,0.8889895278168062,-0.017174260409137283,0.004614250484695657,-1.1537064635161052]]]
        self.default_config['params'][1]['trapezoid_coords'] = ['list', [[1125,403],[1920,201],[1126,897],[1919,1055]]]
        # self.default_config['description'] = "Deskrypszyn"
        # self.default_config['id'] = "Jakie niby ID?!?!"

    def setup(self):
        self.input_classes = {
            "color": stream_video.Consumer,
            "metrics": stream_data.Consumer,
        }
        self.output_classes = {
            "color": stream_video.Producer,
            "metrics": stream_data.Producer
        }
        


    def task_process(self, input_task_data, input_stream):
        """przetwarzanie strumieni"""

        tc = self.params.get('trapezoid_coords', self.default_config['params'][1]['trapezoid_coords'][1])
        trapezoid_coords = np.array(tc)
        # trapezoid_coords = self.params.get('trapezoid_coords_CUSTNAME')

        """get parameters for Wisenet camera calibration"""
        mtx_list = self.params.get("mtx", self.default_config['params'][1]['mtx'][1])
        dist_list = self.params.get("dist", self.default_config['params'][1]['dist'][1])
        mtx = np.array(mtx_list)
        dist = np.array(dist_list)

        with self.task_emit(input_task_data) as output_stream:
            runonce_flag = 0
            for input_data in input_stream:
                begin = time.time()

                if runonce_flag == 0:
                    M, W, H = get_perspective(input_data['color'], trapezoid_coords)
                    print('Mtx, W, H')
                    runonce_flag = 1
                """undistort"""
                undist_frame = cv2.undistort(input_data['color'], mtx, dist, None, mtx)
                # in_transformed = cv2.warpPerspective(input_data['color'], M, (W, H))
                in_transformed = cv2.warpPerspective(undist_frame, M, (W, H))
                print(f"czas wykonania: {time.time() - begin} s")

                output_data = {
                    "color": in_transformed,
                    "metrics": input_data["metrics"]
                }

                output_stream.emit(output_data)


if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()
