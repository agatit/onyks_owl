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
        last_frame = None
        period = time.time()
        frame_buffer = []
        buffer_size = 25
        compared_value = 150000
        frame_counter = 0
        state = 0
        last_state = 0
        for input_data in input_stream:
            frame = input_data   
            if len(frame_buffer) > 9:
                dframe = cv2.absdiff(frame, frame_buffer[-5])
                gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                pixel_count = cv2.countNonZero(bwframe)
                
                #wybieranie na którym torze jest większy ruch:
                if pixel_count > compared_value:
                    state = 1
                    print("state:", bool(state))
                else:
                    state = 0
                    print("state:", bool(state))
                    
                if state == 1 or frame_counter < buffer_size:
                    print("last_state_in_loop:", last_state)
                    if state == 1 and last_state == 0:
                        #output_task_data = input_task_data 
                        output_stream = self.task_emit(input_task_data)
                        print("1234")
                    
                    if state == 0:
                        frame_counter += 1
                        if frame_counter > buffer_size:
                            output_stream.end()
                    else:
                        frame_counter = 0                               
                output_stream.emit(input_data)   
            last_state = state
            print("last_state:", last_state)
                    
            frame_buffer.append(frame)
            if len(frame_buffer) > buffer_size:
                frame_buffer.pop(0)
            frame = input_data


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        