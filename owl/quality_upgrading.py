# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Poprawienie jakosci pociagu"""

import os
import sys
import json
import logging
import cv2
import redis
import time
import task
import stream_video
import stream_data
import module_base
import math
import numpy

frame_tab = []


class Module(module_base.Module):
    def streams_init(self): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {
            "color": stream_video.Producer ,
            "metrics": stream_data.Producer
        }


    def task_process(self, input_task_data, input_stream ):
        "mierzenie prędkosci pociagu"

        delay = self.params.get("delay", 5)     #musi byc taka sama jak w velocitymeasure 

        output_data = {}
        output_able = False

        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:     
                print("task!") 
                begin = time.time()          
                output_data['color'] = input_data['color']
                output_data['metrics'] = input_data['metrics']
                output_data['metrics']['velocity'] = 0
                output_data['metrics']['standard deviation'] = 0
                
                standard_deviation_shift = 0
                average_shift = 0

                
                #przypisanie do frame obrazu i zrobienie delaya#

                frame = input_data['color']                                     
                #frame = frame[p1_c[0]:p2_c[0],p1_c[1]:p2_c[1]]
                frame_tab.append(frame)
                frame_delayed = frame_tab[0]
                if len(frame_tab) > delay:
                    frame_delayed = frame_tab.pop(0) 

                #odczytanie predkosci
                velocity = input_data['metric']['velocity']

                if velocity[0]>0:
                    

                             
         

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()