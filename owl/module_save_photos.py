# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Zapisywanie zdjęć do późniejszego douczania"""

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
        "Zapisywanie zdjec do douczania"
        folder= self.params.get("folder", "sciezka")
        emit = self.params.get("emit", 0)

        dirName = os.path.join(folder, "photos_to_relearn")
        # Create target directory & all intermediate directories if don't exists
        try:
            os.makedirs(dirName)    
            print("Directory " , dirName ,  " Created ")
            
        except FileExistsError:
            print("Directory " , dirName ,  " already exists") 

        output_data = {}
        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:      

                cv2.imwrite(os.path.join(dirName,f'{time.time()}.jpg'),input_data['color'])

                if emit == 1:
                    output_data['color'] = input_data['color']
                    output_data['metrics'] = input_data['metrics']          
                    output_stream.emit(output_data) 

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()