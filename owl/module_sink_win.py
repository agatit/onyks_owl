# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł wyświtlający strumien video"""

import os
import sys
import json
import logging
import cv2
import redis
import task
import stream_video
import stream_data
import module_base


class Module(module_base.Module):
    def __init__(self, argv):
        super(Module, self).__init__(argv)
        self.default_config['params'][1]['window_name'] = ['string', 'noname']

    def setup(self): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {}


    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        window_name = self.params.get('window_name', input_task_data.get('source_name', 'noname'))
        if 'railtrack' in input_task_data:
            window_name = f"{window_name}_{input_task_data['railtrack']}"
        
        for input_data in input_stream:            
            cv2.imshow(window_name, input_data['color'])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()