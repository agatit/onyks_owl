# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł sprawdzajacy obecnosc tablicy z numerem wagonu"""

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

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
frame_tab = []
shift_tab = []

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

        delay = self.params.get("delay", 5)
        points = self.params.get("points", 20)
        p1_c = self.params.get("p1_c", [0,0])
        p2_c = self.params.get("p2_c", [3000,3000])
        dis_min = self.params.get("dis_min", 10)
        klasa_dokladnosci_predkosci = self.params.get("klasa_dokladnosci_predkosci", 10)
        shift_min = self.params.get("shift_min", 10)
        shift_max = self.params.get("shift_max", 20)
        y_max = self.params.get("y_max", 3)
        min_factor = self.params.get("min_factor", 0.8)
        max_factor = self. params.get("max_factor", 1.4)
        debug = self.params.get("debug", 0)

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

                
                frame = input_data['color']
                #frame = frame[p1_c[0]:p2_c[0],p1_c[1]:p2_c[1]]
                frame_tab.append(frame)
                frame_delayed = frame_tab[0]
                if len(frame_tab) > delay:
                    frame_delayed = frame_tab.pop(0)                
               
                if len(frame_tab)==delay:
                    kp1, des1 = orb.detectAndCompute(frame,None)
                    kp2, des2 = orb.detectAndCompute(frame_delayed,None)
                    matches = bf.match(des1,des2)
                    matches = sorted(matches, key = lambda x:x.distance)

                    shift_matches = 0
                    i_matches = 0
                    frame_BF = frame
                    for match in matches[:points]:
                        p1 = kp1[match.queryIdx].pt
                        p2 = kp2[match.trainIdx].pt
                        
                        #obliczanie predkosci
                        x_dis = int(p1[0])-int(p2[0])
                        x_2 = x_dis*x_dis
                        y_dis = (int(p1[1])-int(p2[1]))^2
                        y_2 = y_dis*y_dis
                        sum_dis = x_2 + y_2
                        dis = math.sqrt(sum_dis)
                        shift = dis/delay
                        #usrednianie predkosci
                        if shift > shift_min and shift < shift_max and y_dis <y_max:                   
                            shift_matches = shift_matches + shift       
                            i_matches = i_matches + 1
                            
                            

                    if i_matches != 0:
                        shift_frame = shift_matches/i_matches
                    else:
                        shift_frame = 0
                        
                    
                    
                    if shift_frame !=0:
                        shift_tab.append(shift_frame)
                        if len(shift_tab) > klasa_dokladnosci_predkosci:
                            trash = shift_tab.pop(0)
                            shift_min = min_factor*average_shift
                            shift_max = max_factor*average_shift
                        average_shift = sum(shift_tab)/len(shift_tab)
                        standard_deviation_shift = numpy.var(shift_tab, ddof=1)
                        output_able = True
                        output_data['metrics']['velocity'] = average_shift
                        output_data['metrics']['standard deviation'] = standard_deviation_shift

                    if debug == 1:
                        if output_able:
                            cv2.line(frame_BF,(int(p1[0]),int(p1[1])),(int(p2[0]), int(p2[1]) ),(255,0,0), 5)
                    
                logging.info(f" {standard_deviation_shift} {average_shift} {time.time() - begin}")
                
                    
                output_stream.emit(output_data)     

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()