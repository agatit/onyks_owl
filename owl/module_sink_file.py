# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł zapisujący strumień do pliku video"""

import os
import sys
import json
import logging
from datetime import datetime
import cv2
import redis
import task
import stream_video
import stream_data
import module_base


class Module(module_base.Module):
    def setup(self): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {}     
    
    def task_process(self, input_task_data, input_stream ):
        'zapis strumienia do pliku'

        frame_no = 0
        filename = ""
        out = None
        print(input_stream)
        for input_data in input_stream:
            frame = input_data['color']
            if frame_no == 0:
                fourcc_str = self.params.get('fourcc', 'XVID')
                fourcc = cv2.VideoWriter_fourcc(*fourcc_str)          
                      
                filename = self.params.get('filename', input_task_data.get('source_name', 'noname')) # TODO ścieżka do out'a projektu czy coś takiego
                print("filename: " + filename)
                if 'railtrack' in input_task_data:
                    filename += f"_{input_task_data['railtrack']}"
                filename = datetime.now().strftime(filename)
                filename = os.path.join(self.params.get('path',"."), filename)

                framerate = self.params.get('framerate', 20.0)
                height, width = frame.shape[0:2]
                self.log_object.info(f"file {filename} writing started (fourcc:{fourcc_str} framerate:{framerate} size:{(width, height)})")
                out = cv2.VideoWriter(filename, fourcc, framerate, (width, height))
            out.write(frame)
            frame_no += 1  
        
        if out:
            out.release()
            print("out_released")
        self.log_object.info(f"file {filename} writing finished")
        

if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()