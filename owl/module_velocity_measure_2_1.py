# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Moduł mierzacy predkosc pociagu  opcja z srednią i dostosowywaniem się do mediany """
            #wprowadzone zmiany: 
            #                   modul ocr zmieniony na opticalflow
            #                
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
import numpy as np

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

counter_tab = np.array([-1,1,1])



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

        the_limit_of_stillness = self.params.get("the_limit_of_stillness", 5)
        y_max_velocity = self.params.get("y_max_velocity", 2)
        x_max_velocity = self.params.get("x_max_velocity", 20)
        x_min_velocity = self.params.get("x_min_velocity", 5)
        v_f_tab = self.params.get("v_f_tab", [])
        velocity_accuracy_class = self.params.get("velocity_accuracy_class", 50)
        minimum_number_of_points = self.params.get("minimum_number_of_points", 15)
        min_v_tab_length = self.params.get("min_v_tab_length", 15)
        max_v_tab_length = self.params.get("max_v_tab_length", 100)
        debug = self.params.get("debug", 0)
        deviation = self.params.get("deviation", 2)
        velocity = 0 
        output_data = {}
        first_frame = True
        average_v_f = 0

        with self.task_emit({}) as output_stream: 
            for input_data in input_stream:     
                print("task!") 
                begin = time.time()          
                output_data['color'] = input_data['color']
                output_data['metrics'] = input_data['metrics']
                output_data['metrics']['velocity'] = 0
        ################################# rzeczywiste dzialanie modulu ########################

        # Take first frame and find corners in it
                if first_frame:
                    old_frame = input_data['color']
                    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
                    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)


                    counter_tab =  np.zeros((len(p0),1,1))
                    p0_min = len(p0)/2

                    # Create a mask image for drawing purposes
                    mask = np.zeros_like(old_frame)
                    first_frame = False
                else:
                    frame = input_data['color']
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # calculate optical flow
                    if len(p0)> minimum_number_of_points:                                                                                              #na wypadek jakby weszło z zerową liczbą dobrych punktów 

                        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

                    else:
                        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

                        counter_tab = np.zeros((len(p0), 1,1))
                        p0_min = len(p0)/2
                        
                        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
                        # print("dodalem nowe punkty")
                    
                    for i, any in enumerate(counter_tab):                                                                          #sprawdz czy punkty nie są zbyt dlugo bez ruchu
                        if counter_tab[i,0,0] >= the_limit_of_stillness:
                            st[i] = 0


                    
                    
                    # Select good points
                    if np.any(st != 0):                                                                                             #jezeli nie wszystkie punkty zostały wykreslone bo staly
                        good_new = p1[st==1]
                        good_old = p0[st==1]
                        counter_tab_temp = counter_tab[st==1]                                                                           #to zrob z nich listy aktualnych punktów 
                    

                    else:
                        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

                        counter_tab = np.zeros((len(p0), 1))
                        p0_min = len(p0)/2
                        
                        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

                        good_new = p1[st==1]
                        good_old = p0[st==1]
                        counter_tab_temp = counter_tab[st==1]                                                                    #jezeli punktow nie bylo to znajdz nowe i zrob na ich podstawie liste aktualnych punktow
                    




                ####################################################################                  OBLICZANIE PREDKOSCI                         ###########################################################################    

                    v_p = []
                    for i,(new,old) in enumerate(zip(good_new, good_old)):
                        a,b = new.ravel()
                        c,d = old.ravel()

                        if len(v_f_tab) < min_v_tab_length or v_f_tab is not None:
                            if abs(int(b) - int(d)) < y_max_velocity and abs(int(a) - int(c)) >x_min_velocity and abs(int(a) - int(c)) < x_max_velocity: 
                                v_p.append(a - c)
                                counter_tab_temp[i] = 0
                                if debug:
                                    mask = cv2.line(mask, (int(a),int(b)),(int(c),int(d)), (255,0,0), 2)
                                    frame = cv2.circle(frame,(int(a),int(b)),5,(0,255,0),-1)
                                    frame = cv2.circle(frame,(int(c),int(d)),5,(0,150,150),-1)
                            else:
                                
                                counter_tab_temp[i] = counter_tab_temp[i] +1
                                if debug:
                                    frame = cv2.circle(frame,(int(c),int(d)),5,(0,0,255),-1)
                                    frame = cv2.putText(frame,str(counter_tab_temp[i]),(int(a), int(b)),cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255), 1)
                        
                        if len(v_f_tab) > min_v_tab_length:
                            if abs(int(b) - int(d)) < y_max_velocity and abs(int(a) - int(c)) >np.median(v_f_tab)-deviation and abs(int(a) - int(c)) < np.median(v_f_tab)+deviation: 
                                v_p.append(a - c)
                                counter_tab_temp[i] = 0
                                if debug:
                                    mask = cv2.line(mask, (int(a),int(b)),(int(c),int(d)), (255,0,0), 2)
                                    frame = cv2.circle(frame,(int(a),int(b)),5,(0,255,0),-1)
                                    frame = cv2.circle(frame,(int(c),int(d)),5,(0,150,150),-1)
                            else:
                                
                                counter_tab_temp[i] = counter_tab_temp[i] +1
                                if debug:
                                    frame = cv2.circle(frame,(int(c),int(d)),5,(0,0,255),-1)
                                    frame = cv2.putText(frame,str(counter_tab_temp[i]),(int(a), int(b)),cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255), 1)
                            

                            
                            



                    
                    
                    v_f = np.median(v_p)
                    if not np.isnan(v_f):
                        v_f_tab.append(v_f)
                        if len(v_f_tab) > min_v_tab_length:
                            average_v_f = np.average(v_f_tab)
                        if len(v_f_tab) > max_v_tab_length:
                            trash =v_f_tab.pop(0)
                            
                    
                    

                #############################################################                LACZENIE OBRAZOW W JEDNO I WYSWIETLANIE                           ###############################################################
                    
                    img = cv2.add(frame,mask)
                    if debug:
                        cv2.imshow('frame',img)
                        print(average_v_f)
                        k = cv2.waitKey(30) & 0xff
                    if k == 27:
                        break


                ################################################################                PRZENOSZENIE DANYCH NA NASTEPNA KLATKE                     ###################################################################  

                    counter_tab = counter_tab_temp.reshape(-1,1,1)
                    old_gray = frame_gray.copy()
                    p0 = good_new.reshape(-1,1,2)

                        
            ################################# koncowe wysylanie rzeczy ############################
                    output_data['metrics']['velocity'] = average_v_f   
                    output_stream.emit(output_data)   

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()