# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł mierzacy predkosc pociagu"""
            #wprowadzone zmiany: 
            #                   velocity podzielone na wektor dwuelementowy 
            #                   wysylanie tylko tych color które mają na sobie wykryty jadący pociąg 

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
from statistics import median

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
frame_tab = []
shift_tab_x = []
shift_tab_y = []

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
   
        klasa_dokladnosci_predkosci = self.params.get("klasa_dokladnosci_predkosci", 10)
        shift_min = self.params.get("shift_min", 10)
        shift_max = self.params.get("shift_max", 20)
        y_max = self.params.get("y_max", 3)
       
        debug = self.params.get("debug", 0)
        deviation = self.params.get("deviation", 3)

        output_data = {}
        output_able = False
        med_shift_tab = []

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

                    shift_matches_x = 0
                    shift_matches_y = 0
                    i_matches = 0
                    frame_BF = frame
                    for match in matches[:points]:
                        p1 = kp1[match.queryIdx].pt
                        p2 = kp2[match.trainIdx].pt
                        
                        #obliczanie predkosci
                        x_dis = int(p1[0])-int(p2[0])
                        y_dis = (int(p1[1])-int(p2[1]))
                        shift_x = x_dis/delay
                        shift_y = y_dis/delay
                        
                        #metoda mediany
                        if len(med_shift_tab) < 10:
                            if abs(shift_x) > shift_min and abs(shift_x) < shift_max and shift_y < y_max:
                                med_shift_tab.append(shift_x)
                            else:
                                shift_x = 0
                        elif len(med_shift_tab) >=10 and len(med_shift_tab) <50:
                            if shift_x > median(med_shift_tab)-deviation and shift_x < median(med_shift_tab)+deviation:
                                med_shift_tab.append(shift_x)
                            else:
                                shift_x = 0
                        elif len(med_shift_tab) == 50:
                            if shift_x > median(med_shift_tab)-deviation and shift_x < median(med_shift_tab)+deviation:
                                thrash = med_shift_tab.pop(0)
                                med_shift_tab.append(shift_x)
                            else:
                                shift_x = 0
                        
                        if shift_x != 0:                   
                            shift_matches_x = shift_matches_x + shift_x 
                            shift_matches_y = shift_matches_y + shift_y     #odrzuc predkosci w pionie 
                            i_matches = i_matches + 1
                    if i_matches != 0:
                        shift_frame_x = shift_matches_x/i_matches
                        shift_frame_y = shift_matches_y/i_matches 
                    else:
                        shift_frame_x = 0
                        shift_frame_y = 0
                        
                    if shift_frame_x !=0:
                        shift_tab_x.append(shift_frame_x)
                        shift_tab_y.append(shift_frame_y)
                        if len(shift_tab_x) > klasa_dokladnosci_predkosci:
                            trash_x = shift_tab_x.pop(0)
                            trash_y = shift_tab_y.pop(0)
                            shift_min = 0.8*abs(average_shift_x)
                            shift_max = 1.4*abs(average_shift_x)
                        average_shift_x = sum(shift_tab_x)/len(shift_tab_x)
                        print(average_shift_x)
                        average_shift_y = sum(shift_tab_y)/len(shift_tab_y)
                        there_is_no_move = 0
                        #print(average_shift_y)
                    else:
                        there_is_no_move = there_is_no_move + 1

                    
                    if there_is_no_move == 15:
                        med_shift_tab.clear()
                        there_is_no_move = 0
                    
                    if shift_frame_x !=0:
                        shift_tab_x.append(shift_frame_x)
                        shift_tab_y.append(shift_frame_y)
                        if len(shift_tab_x) > klasa_dokladnosci_predkosci:
                            trash_x = shift_tab_x.pop(0)
                            trash_y = shift_tab_y.pop(0)
                            shift_min = 0.8*abs(average_shift_x)
                            shift_max = 1.4*abs(average_shift_x)
                        average_shift_x = sum(shift_tab_x)/len(shift_tab_x)
                        print(average_shift_x)
                        average_shift_y = sum(shift_tab_y)/len(shift_tab_y)
                        print(f" average_shift_y")
                        average_shift=[average_shift_x,average_shift_y]
                        standard_deviation_shift_x = numpy.var(shift_tab_x, ddof=1)
                        standard_deviation_shift_y = numpy.var(shift_tab_y, ddof=1)
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