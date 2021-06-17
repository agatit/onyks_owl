# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł wyświtlający strumien video"""

import os
import sys
import json
import logging
import time

import cv2
import redis
import task
import stream_video
import stream_data
import module_base


class Module(module_base.Module):
    def streams_init(self): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {}


    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'
        
        for input_data in input_stream:
            begin = time.time()
            cv2.imshow(self.params.get('window_name', 'noname'), input_data['color'])
            print(f"czas po jakim wyswietla sie kolejny frame: {time.time() - begin} s")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()