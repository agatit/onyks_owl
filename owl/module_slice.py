# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł rozdzielający strumień obrazu na zadania"""

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
    def streams_init(self): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }


    def task_process(self, input_task_data, input_stream ):
        """przetwarzanie strumieni"""

        frame_count = self.params.get('frame_count', 1000)
        frame_no = 0
        slice_no = 0

        for input_data in input_stream:             
            if frame_no < frame_count:
                if frame_no == 0:
                    output_task_data = {}
                    output_task_data['slice_no'] = slice_no
                    output_stream = self.task_emit(output_task_data)
                    detection = False 
                metrics = input_data['metrics']
                metrics["frame_no"] = frame_no
                output_data = {"color" : input_data['color'], "metrics" : metrics}                      
                output_stream.emit(output_data) 
                frame_no += 1
            else:      
                output_stream.end()  
                logging.info("end of slice")
                frame_no = 0
                slice_no += 1
        
        logging.info("input task done")
        


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()