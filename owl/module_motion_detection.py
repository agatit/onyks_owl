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
        head_frames = self.params.get("head_frames", 100)
        tail_frames = self.params.get("tail_frames", 100)
        frames_treshold = self.params.get("frames_treshold", 10)
        pixels_treshold = self.params.get("pixels_treshold", 50000)
        frame_gap = self.params.get("frame_gap", 5)
        motion_state = False
        motion_frames = 0
        left_frames = 0

        for input_data in input_stream:
            begin = time.time()
            output_data = input_data

            if len(frame_buffer) == head_frames:
                dframe = cv2.absdiff(input_data['color'], frame_buffer[-frame_gap]['color'])
                gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                pixel_count = cv2.countNonZero(bwframe)
                if pixel_count > pixels_treshold:
                    motion_frames += 1
                    print(f"motion_frames: {motion_frames} frames in motion:{motion_frames/frames_treshold:.2f}")
                else:
                    motion_frames = 0                    
                motion_state = motion_frames >= frames_treshold
            else:
                motion_state = False
                        
            #TODO: wybieranie na którym torze jest największy ruch            
            output_task_data['railtrack'] = "0"

            if motion_state:
                if not output_stream:                        
                    logging.debug("Motion begin")
                    output_stream = self.task_emit(output_task_data)                    
                left_frames = len(frame_buffer) + tail_frames

            if output_stream:
                if left_frames > 0:                
                    output_stream.emit(frame_buffer[0])
                    left_frames -= 1                                 
                else:
                    logging.debug("Motion end")
                    output_stream.end()
                    output_stream = None                    

            frame_buffer.append(output_data)
            if len(frame_buffer) > head_frames:                
                frame_buffer.pop(0) # zbyt stara -> do śmieci
        
        logging.debug("End of motion task")

        # na wypadek zakończenia strumienia wejściowego podczas ruchu - emitujemy ogon
        if output_stream:
            logging.debug("Write down tail of stream")
            while left_frames > 0 and len(frame_buffer) > 0:
                output_stream.emit(frame_buffer.pop(0))              
                left_frames -= 1


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        