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
import task
import stream_video
import stream_data
import module_base

hopefully_train_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")


class Module(module_base.Module):
    def __init__(self, argv): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {
            "color": stream_video.Producer ,
            "metrics": stream_data.Producer
        }
        super().__init__(argv)  

    def task_process(self, input_task_data, input_stream ):
        "sprawdzanie czy jest pociag"
        
        factor = self.params.get("factor", 1.1)
        neighbour = self.params.get("neighbour", 4)
        debug = self.params.get("debug", 0)

        output_data = {}

        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:                
                output_data['color'] = input_data['color']
                output_data['metrics'] = input_data['metrics']
                output_data['metrics']['detected_plates'] = []

                gray = cv2.cvtColor(input_data['color'], cv2.COLOR_BGRA2GRAY)                
                detected_plates = hopefully_train_cascade.detectMultiScale(gray, factor, neighbour)                
                for (x,y,w,h) in detected_plates: 
                    output_data['metrics']['detected_plates'].append([int(x), int(y), int(w), int(h)])
                    if debug == 1:
                        output_data['color'] = cv2.rectangle(output_data['color'], (x, y), (x+w, y+h), (255,0,0), 5)                                        
                    
                print(output_data['metrics'])
                output_stream.emit(output_data)     

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()