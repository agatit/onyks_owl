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
            rt.setdefault("distance_treshold", 5)
            rt.setdefault("frames_treshold", 10)
            rt.setdefault("pixels_treshold", 50)
            rt.setdefault("frame_gap", 2)
            rt.setdefault("debug", False)
            rt.setdefault("overlaps", [])
            rt['initial_mask'] = np.zeros(image_size, dtype=np.uint8)
            cv2.fillPoly(rt['initial_mask'], np.array([rt['roi']], dtype=np.int32), [255])              

            if self.params['debug']:
                cv2.imshow(rt['name'], rt['initial_mask'])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

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
                is_first_frame = False
                input_size = input_data['color'].shape
                for rt in self.railtracks:
                    rt['mask'] = cv2.resize(rt['initial_mask'], (input_size[1], input_size[0]))                  
                    pixel_count = cv2.countNonZero(rt['mask'])
                    rt['pixel_count_treshold'] = int(pixel_count * rt['pixels_treshold'] / 100)

            for rt in self.railtracks:
                if len(frame_buffer) == rt['head_frames']:
                    # wyznaczanie obszaru ruchu
                    dframe = cv2.absdiff(input_data['color'], frame_buffer[-rt['frame_gap']]['color'])
                    gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
                    ret, bwframe = cv2.threshold(gdframe,rt['distance_treshold'],255,cv2.THRESH_BINARY)

                    # maskowanie maską toru
                    rt['masked_bwframe'] = cv2.bitwise_and(bwframe, rt['mask'])     

                    pixel_count = cv2.countNonZero(rt['masked_bwframe'])
                    
                    # filtrowanie progiem liczby ruchomych ramek
                    if pixel_count > rt['pixel_count_treshold']:
                        rt['motion_frames'] += 1
                    else:
                        rt['motion_frames'] = 0                    
                    rt['motion_state'] = rt['motion_frames'] >= rt['frames_treshold']
                    
                    # sprawdzenie czy nie ma ruchu na torze zasłaniającym
                    if rt['motion_state'] and any(
                                            map(lambda r: r["motion_state"],
                                            filter(lambda r: rt['name'] in r["overlaps"], self.railtracks))):
                        rt['motion_state'] = False
                        rt['motion_frames'] = 0

                else:
                    rt['motion_state'] = False                                

                # obsługa wykrycia ruchu -> task
                if rt['motion_state']:
                    if not rt['output_stream']:                        
                        logging.debug(f"Motion begin on {rt['name']}")
                        output_task_data["railtrack"] = rt['name']
                        rt['output_stream'] = self.task_emit(output_task_data)                                    
                    rt['left_frames'] = min(rt['head_frames'], len(frame_buffer)) + rt['tail_frames']

                # generowanie i zakończenie strumieni wyjsciowych
                if rt['output_stream']:                       
                    if rt['left_frames'] > 0:   
                        if self.params['debug'] and rt['masked_bwframe'] is not None:
                            frame_buffer[0]['color'] = cv2.cvtColor(rt['masked_bwframe'], cv2.COLOR_GRAY2BGR)
                        rt['output_stream'].emit(frame_buffer[0])
                        rt['left_frames'] -= 1                               
                    else:
                        logging.debug(f"Motion end on {rt['name']}")
                        rt['output_stream'].end()
                        rt['output_stream'] = None                        

            # rotacja bufora
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
                rt['output_stream'].end()

        if begin + 0.1 < time.time():
            logging.debug(f"Processing time: {time.time() - begin}")


if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()
        