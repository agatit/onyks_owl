from operator import mod
import numpy as np
import os
import logging
import cv2
import sys
import redis
import task
import json
import time
import stream_composed
import stream_video
import stream_data
import module_base

# Moduł do detekcji pociągów:

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
    
    def task_process(self, input_task_data, input_stream):    
        
        output_task_data = input_task_data
        frame_buffer = []
        output_stream = None
        buffer_size = self.params.get("buffer_size", 25)
        pixel_treshold = self.params.get("pixel_treshold", 0)
        frame_gap = self.params.get("frame_gap", 5)
        motion_state = False
        frame_tail = 0

        for input_data in input_stream:
            begin = time.time()
            output_data = input_data

            if len(frame_buffer) == buffer_size:
                dframe = cv2.absdiff(input_data['color'], frame_buffer[-frame_gap]['color'])
                gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                pixel_count = cv2.countNonZero(bwframe)
                motion_state =  pixel_count > pixel_treshold
            else:
                motion_state = False
                        
            #TODO: wybieranie na którym torze jest największy ruch            
            output_task_data['railtrack'] = "0"

            if motion_state:
                if not output_stream:                        
                    logging.debug("Motion begin")
                    output_stream = self.task_emit(output_task_data)                    
                frame_tail = len(frame_buffer)

            if output_stream:
                if frame_tail > 0:                
                    output_stream.emit(frame_buffer[0])
                    frame_tail -= 1                    
                else:
                    logging.debug("Motion end")
                    output_stream.end()
                    output_stream = None                    

            frame_buffer.append(output_data)
            if len(frame_buffer) > buffer_size:                
                frame_buffer.pop(0) # do śmieci
        
        # na wypadek zakończenia strumienia wejściowego podczas ruchu - emitujemy ogon
        if output_stream:
            while frame_tail > 0 and len(frame_buffer) > 0:
                output_stream.emit(frame_buffer.pop(0))              
                frame_tail -= 1


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        