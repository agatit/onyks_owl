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
import copy

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
    def getDisp(self, imgL, imgR):
        # logging.info(imgL.keys())
        # logging.info(imgR.shape())
        left_for_matcher = cv2.cvtColor(imgL,  cv2.COLOR_BGR2GRAY)
        right_for_matcher = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

        left_disp = self.left_matcher.compute(left_for_matcher, right_for_matcher)
        right_disp = self.right_matcher.compute(right_for_matcher, left_for_matcher)

        filtered_disp = self.wls_filter.filter(left_disp,imgL,disparity_map_right=right_disp)

        vis = cv2.ximgproc.getDisparityVis(filtered_disp)
        disp = cv2.normalize(vis, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
        
        disp2 = np.dstack((disp, disp, disp))
        return disp2
    def task_process(self, input_task_data, input_stream):    

        wls_lambda = self.params.get("wls_lambda", 8000)
        wls_sigma = self.params.get("wls_sigma", 1.5)
        self.left_matcher = cv2.StereoSGBM_create()
        self.wls_filter = cv2.ximgproc.createDisparityWLSFilter(self.left_matcher)
        self.wls_filter.setLambda(wls_lambda)
        self.wls_filter.setSigmaColor(wls_sigma)
        self.right_matcher = cv2.ximgproc.createRightMatcher(self.left_matcher)
        cv2.namedWindow('xddd', cv2.WINDOW_FREERATIO)
        output_task_data = input_task_data
        buffer_size = self.params.get("buffer_size", 2)
        frame_buffer = []
        output_stream = None
        motion_state = False
        frame_tail = 0
        for input_data in input_stream:
            begin = time.time()

            if len(frame_buffer) == buffer_size:
                output_frame = copy.deepcopy(input_data)
                cv2.imshow('xddd', frame_buffer[0]['color'])
                cv2.waitKey(1)
                output_frame['color'] = self.getDisp(frame_buffer[0]['color'], frame_buffer[buffer_size-1]['color'])
                logging.debug("Output frame made")
                
                if not output_stream:
                    logging.debug("Material begin")
                    output_stream = self.task_emit(output_task_data)
                    logging.debug("Output stream created")
                output_stream.emit(output_frame)
                logging.debug("Output frame send")
            frame_buffer.append(input_data)
            logging.debug("Frame appended")
            if len(frame_buffer) > buffer_size:
                logging.debug("OY! There's too much frames mate!")
                frame_buffer.pop(0) # do śmieci
                logging.debug("Frame yeet'ed")
        logging.debug("Material end")
        output_stream.end()
        output_stream = None
        
        # na wypadek zakończenia strumienia wejściowego podczas ruchu - emitujemy ogon
        # if output_stream:
        #     while frame_tail > 0 and len(frame_buffer) > 0:
        #         output_stream.emit(frame_buffer.pop(0))              
        #         frame_tail -= 1


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
        