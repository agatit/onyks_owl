# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł sprawdzajacy obecnosc tablicy z numerem wagonu"""

import os
import sys
import json
import logging
import cv2
import redis
import time
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
        self.output_classes = {
            "color": stream_video.Producer ,
            "metrics": stream_data.Producer
        }


    def task_process(self, input_task_data, input_stream ):
        "Przecedzanie co którejś klatki"
        
        ratio = self.params.get("ratio", 2)
        debug = self.params.get("debug", 0)

        output_data = {}
        frame_number = 0
        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:      
                begin = time.time()
                frame_number += 1
                if frame_number >= ratio:
                    frame_number = 0
                    output_data['color'] = input_data['color']
                    output_data['metrics'] = input_data['metrics']          
                    output_stream.emit(output_data) 
                if debug == 1:    
                    logging.info(f"execution time: {time.time() - begin}")

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()