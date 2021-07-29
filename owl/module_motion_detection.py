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

        # TODO: obsłuzyć sytuację gdy nie istnieje definicja railtracks
        self.railtracks = self.params['railtracks']
        image_size = self.params.get("image_size",(1080, 1920))
         
        for rt in self.railtracks:                                    
            rt.setdefault("head_frames", 100)
            rt.setdefault("tail_frames", 100)
            rt.setdefault("frames_treshold", 10)
            rt.setdefault("pixels_treshold", 50000)
            rt.setdefault("frame_gap", 5)
            rt['initial_mask'] = np.zeros(image_size, dtype=np.uint8)
            cv2.fillPoly(rt['initial_mask'], np.array([rt['roi']], dtype=np.int32), [255])              
    

    def task_process(self, input_task_data, input_stream):    
        
        output_task_data = input_task_data
        frame_buffer = []
        is_first_frame = True
        max_head_frames = max(rt['head_frames'] for rt in self.railtracks)

        for rt in self.railtracks:
            rt['output_stream'] = None
            rt['motion_state'] = False
            rt['motion_frames'] = 0
            rt['left_frames'] = 0
    
        for input_data in input_stream:
            begin = time.time()
            output_data = input_data

            if is_first_frame:
                for rt in self.railtracks:
                    is_first_frame = False

                    input_size = input_data['color'].shape
                    rt['mask'] = cv2.resize(rt['initial_mask'], (input_size[1], input_size[0]))

            for rt in self.railtracks:
                if len(frame_buffer) == rt['head_frames']:
                    dframe = cv2.absdiff(input_data['color'], frame_buffer[-rt['frame_gap']]['color'])
                    gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                    ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
                    masked_bwframe = cv2.bitwise_and(bwframe, rt['mask']) 
                    pixel_count = cv2.countNonZero(masked_bwframe)
                    if pixel_count > rt['pixels_treshold']:
                        motion_frames += 1
                        print(f"motion_frames: {motion_frames} frames in motion:{motion_frames/rt['frames_treshold']:.2f}")
                    else:
                        motion_frames = 0                    
                    motion_state = motion_frames >= rt['frames_treshold']
                else:
                    motion_state = False
                            
                #TODO: wybieranie na którym torze jest największy ruch            
                output_task_data['railtrack'] = "0"

                if motion_state:
                    if not rt['output_stream']:                        
                        logging.debug("Motion begin")
                        rt['output_stream'] = self.task_emit(output_task_data)                    
                    left_frames = len(frame_buffer) + rt['tail_frames']

                if rt['output_stream']:
                    if left_frames > 0:                
                        rt['output_stream'].emit(frame_buffer[0])
                        left_frames -= 1                                 
                    else:
                        logging.debug("Motion end")
                        rt['output_stream'].end()
                        rt['output_stream'] = None                    

            frame_buffer.append(output_data)
            if len(frame_buffer) > max_head_frames:                
                frame_buffer.pop(0) # zbyt stara -> do śmieci
        
        logging.debug("End of motion task")

        # na wypadek zakończenia strumienia wejściowego podczas ruchu - emitujemy ogon
        for rt in self.railtracks: 
            if rt['output_stream']:
                i = 0
                while rt['left_frames'] > 0 and len(frame_buffer) > i:
                    i += 1
                    rt['output_stream'].emit(frame_buffer[-i])              
                    rt['left_frames'] -= 1                


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        