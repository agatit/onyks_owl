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
        
    def task_process(self, input_task_data, input_stream ):
        for input_data in input_stream:
            #video_stream = cv2.VideoCapture("D:\Agat_IT\onyks_owl-main\onyks_owl-main\owl\out_2_10.mp4")
            last_frame = None
            grabbed, frame = input_stream.read()
            frame_buffer = []
            buffer_size = 25
            compared_value = 150000
            frame_counter = 0
            state = 0
            last_state = 0
            print("grabbed:", grabbed)
            while grabbed:
                period = time.time()
                if len(frame_buffer) > 9:
                    dframe = cv2.absdiff(frame, frame_buffer[-5])
                    gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                    ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                    pixel_count = cv2.countNonZero(bwframe)
                    if pixel_count > compared_value:
                        state = 1
                    else:
                        state = 0
                    if state == 1 or frame_counter < buffer_size:
                        
                        if state == 1 and last_state == 0:
                            output_task_data = input_task_data
                            #dorzucić numer toru 
                            output_stream = self.task_emit(output_task_data)
                            
                            
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
                grabbed, frame = input_stream.read()
                
            input_stream.release()


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        