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
        track_detection0 = False
        track_detection1 = False
        hbf, hf, wbf, wf = 550, 90, 310, 280 #track nr.0
        hbf2, hf2, wbf2, wf2 = 600, 90, 30, 200 #track nr.1
        track_window = (wbf, hbf, wf, hf)
        track_window2 = (wbf2, hbf2, wf2, hf2)
        offset_sum = 50000
        """
        hbf -> height base of frame
        hf -> height of frame
        wbf -> width base of frame
        wf -> width of frame
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
                
            else:
                motion_state = False
                        
            #TODO: wybieranie na którym torze jest największy ruch            
            if len(track_window) == 4 and len(track_window2) == 4:
                if hbf > 0 and hf > 0 and wbf > 0 and wf > 0 and hbf2 > 0 and hf2 > 0 and wbf2 > 0 and wf > 0:
                    roi = input_data['color'][hbf:hbf + hf, wbf:wbf + wf]
                    roi2 = input_data['color'][hbf2:hbf2 + hf2, wbf2:wbf2 + wf2]
                    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    hsv_roi2 = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    mask = np.zeros_like(hsv_roi, dtype="uint8")
                    mask2 = np.zeros_like(hsv_roi2, dtype="uint8")
                    Bit_wised = cv2.bitwise_and(hsv_roi, hsv_roi, mask)
                    Bit_wised2 = cv2.bitwise_and(hsv_roi2, hsv_roi2, mask2)
                    sum_of_roi = np.sum(roi)
                    sum_of_roi2 = np.sum(roi2)
                    print("sum_of_roi:", sum_of_roi)
                    print("sum_of_roi2:", sum_of_roi2)
                    cv2.rectangle(input_data['color'], (wbf, hbf), (wbf+wf, hbf+hf), (255, 0, 0), 2)
                    cv2.rectangle(input_data['color'], (wbf2, hbf2), (wbf2+wf2, hbf2+hf2), (255, 255, 0), 2)
          
                    if sum_of_roi  < sum_of_roi2 + offset_sum:
                        track_detection0 = True
                        print("Detekcja toru 0 udana")
                    else:
                        track_detection0 = False
                        print("Detekcja toru 0 nieudana")
                    
                    if sum_of_roi2 < sum_of_roi + offset_sum:
                        track_detection1 = True
                        print("Detekcja toru 1 udana")
                    else:
                        track_detection1 = False
                        print("Detekcja toru 1 nieudana")
                    
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
        