# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł wyszukujący obiekty na obrazie"""

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
import torch
import numpy

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
        "Wykrywanie obiektów na obrazie"

        weights_path = self.params.get("weights_path", "weights\\yolov5s.pt")
        debug = self.params.get("debug", 0)

        first_frame = 0 
        model = torch.hub.load('ultralytics/yolov5', 'custom', weights_path)
        classes = model.names
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    

        output_data = {}

        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:      
                begin = time.time()      
                results = model(input_data['color'])
                x_shape, y_shape = input_data['color'].shape[1], input_data['color'].shape[0]
                
                labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:,:-1]
                output_data['metrics'] = input_data['metrics'] 
                 
                n = len(labels)
                for i in range(n):
                    row = cord[i]
                    if row[4] >= 0.2:
                        x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                        label = int(labels[i])
                        output_data['metrics']['detection'] = [] 
                        output_data['metrics']['detection'].append([label, x1, y1, x2, y2])   
                        if debug == 1:
                            colour = (0, 255, 0)  
                            cv2.rectangle(input_data['color'], (x1, y1), (x2, y2), colour, 2)


                output_data['color'] = input_data['color']  
                
                    

                output_stream.emit(output_data) 
                if debug == 1:    
                    logging.info(f"execution time: {time.time() - begin}")

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()