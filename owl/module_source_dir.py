# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strunieni video"""
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
        self.input_classes = {}   
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }   


    def task_process(self, input_task_data, input_stream ):
        'przetwarzanie strumieni'
        
        path = self.params.get('path', ".")
        logging.info(f"read dir {path}")
        
        for filename in os.listdir(path):
            logging.info(f"read file {os.path.join(path,filename)}")
            cap = cv2.VideoCapture(os.path.join(path,filename))
            with self.task_emit({}) as output_stream:
                ret,frame = cap.read()
                while(not frame is None): 
                    data = {
                        'color' : frame,
                        'metrics' : {}
                    }
                    output_stream.emit(data)
                    ret,frame = cap.read() 
            cap.release()
            logging.info(f"end of file {os.path.join(path,filename)}")
        logging.info(f"end of dir {path}")


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()