from operator import mod
import numpy as np
import os
import logging
import cv2
import sys
from numpy.core.numeric import count_nonzero
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
        pixel_treshold_counter1 = self.params.get("pixel_treshold_to_counter1", 30000)
        pixel_treshold_counter2 = self.params.get("pixel_treshold_to_counter2", 55000)
        frame_gap = self.params.get("frame_gap", 5)
        motion_state = False
        frame_tail = 0
        track_detection0 = False
        track_detection1 = False
        roi1 = np.array([[(30,565),  
                         (690,705), 
                         (620,610),
                         (190,545)]], dtype=np.int32)
        roi2 = np.array([[(60,655),
                          (660,825),
                          (600,705),
                          (190,610)]], dtype=np.int32)
        """
        roi: (width,height)
        """
        

        for input_data in input_stream:
            begin = time.time()
            output_data = input_data

            if len(frame_buffer) == buffer_size:
                dframe = cv2.absdiff(input_data['color'], frame_buffer[-frame_gap]['color'])
                gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                pixel_count = cv2.countNonZero(bwframe)
                motion_state =  pixel_count > pixel_treshold
                channel_count = dframe.shape[2]
                ignore_mask_color = (255,)*channel_count
                mask1 = np.zeros(bwframe.shape, dtype=np.uint8)
                mask2 = np.zeros(bwframe.shape, dtype=np.uint8)
                cv2.fillPoly(mask1, roi1, ignore_mask_color)
                cv2.fillPoly(mask2, roi2, ignore_mask_color)
                cv2.polylines(input_data['color'], roi1, isClosed=True, color=(255,0,0),thickness=2)
                cv2.polylines(input_data['color'], roi2, isClosed=True, color=(255,255,0),thickness=2)
                masked_frame1 = cv2.bitwise_and(gdframe, mask1) 
                masked_frame2 = cv2.bitwise_and(gdframe, mask2)
                pixel_counter1 = count_nonzero(masked_frame1)
                print("pixel_counter1:", pixel_counter1)
                pixel_counter2 = count_nonzero(masked_frame2)
                print("pixel_counter2:", pixel_counter2)
                if pixel_counter1 > pixel_treshold_counter1:
                    track_detection0 = True
                else:
                    track_detection0 = False
                if pixel_counter2 > pixel_treshold_counter2:
                    track_detection1 = True
                else:
                    track_detection1 = False
            else:
                motion_state = False
                        
            #TODO: wybieranie na którym torze jest największy ruch            
                    
            if motion_state:
                if not output_stream:                        
                    logging.debug("Motion begin")
                    output_stream = self.task_emit(output_task_data)                    
                frame_tail = len(frame_buffer)

            if output_stream:
                if frame_tail > 0:                
                    output_stream.emit(frame_buffer[0])
                    frame_tail -= 1    
                    if track_detection0 == True:
                        output_task_data['railtrack'] = "0"
                        output_stream = self.task_emit(output_task_data) 
                    
                    if track_detection1 == True:
                        output_task_data['railtrack'] = "1"
                        output_stream = self.task_emit(output_task_data)            
                else:
                    logging.debug("Motion end")
                    output_stream.end()
                    output_stream = None                    

            frame_buffer.append(output_data)
            if len(frame_buffer) > buffer_size:                
                frame_buffer.pop(0)
        
        # na wypadek zakończenia strumienia wejściowego podczas ruchu - emitujemy ogon
        if output_stream:
            while frame_tail > 0 and len(frame_buffer) > 0:
                output_stream.emit(frame_buffer.pop(0))              
                frame_tail -= 1


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        