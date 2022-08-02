# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł sprawdzajacy blur"""

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
        "sprawdzenie wielkosci bluru"

        blur_threshold = self.params.get("blur_threshold", 100)
        debug = self.params.get("debug", 0)

        output_data = {}
        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:
                begin = time.time()
                frame = input_data['color']
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                laplacian = cv2.Laplacian(frame_gray, cv2.CV_64F).var()
                if laplacian >= blur_threshold:
                    output_data['color'] = input_data['color']
                    output_data['metrics'] = input_data['metrics']          
                    output_stream.emit(output_data)
                if debug == 1:    
                    logging.info(f"execution time: {time.time() - begin} blur: {laplacian}")


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
