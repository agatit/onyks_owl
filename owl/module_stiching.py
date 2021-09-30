# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Marcin Bak
# Created on: python 3.8.7
"""Poprawienie jakosci pociagu v.2 """

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
img_1 = []
img_2 = []
velocity = 0
velocity_past = 1
max_weight_of_photo = 5000

path = "TUTAJ WPISZ ŚCIEŻKE GDZIE MA ZOSTAĆ ZAPISANE ZDJĘCIE"
global countFolder 
count = 0
count_save =0
counter =0
save_data = True

def save_data_func():
    global countFolder
    countFolder = 0
    while os.path.exists(path + str(countFolder)):
        countFolder = countFolder + 1
    os.makedirs(path + str(countFolder))

if save_data:save_data_func()



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
        "łączenie wszystkich klatek w jeden pociag"
 

        output_data = {}
        output_able = False
        x_pos = 0
        y_pos = 0
        first_frame = True


        with self.task_emit({}) as output_stream:            
            for input_data in input_stream:     
                begin = time.time()          
                output_data['color'] = input_data['color']
                output_data['metrics'] = input_data['metrics']
                output_data['metrics']['velocity'] = input_data['metrics']['velocity']
                velocity_x, velocity_y = input_data['metrics']['velocity']
                

                canva = numpy.zeros_like()
                if velocity_x != 0 or velocity_y != 0:
                    x_pos -= int(velocity_x)
                    y_pos -= int(velocity_y)
                    "tutaj laczenie obrazu"
                    if first_frame:
                        "przypisanie pierwszej klatki do canvy"
                        canva = numpy.zeros(input_data['color'])
                        y_1, x_1, ch_1 = canva.shape
                        y_c, x_c, ch_c = canva.shape
                        alpha = numpy.zeros((y_1, x_1,1), numpy.uint16)
                        first_frame = False
                    else:
                        "rozszerzanie canby i alphy do odpowiedniego polozenia zdjecia"
                        if x_pos > 0  and x_O+x_pos+x_1>x_c:
                            "Poziome przesuniecie w lewo"
                            canva = numpy.hstack((canva, numpy.zeros((y_c, x_pos + x_O + x_1 - x_c, 3), numpy.uint8)))
                            alpha= numpy.hstack((alpha, numpy.zeros((y_c, x_pos + x_O + x_1 - x_c, 1), numpy.uint16)))
                            
                        if x_pos < 0  and abs(x_pos) > x_O:
                            "Poziome przesuniecie w prawo"
                            canva = numpy.hstack((numpy.zeros((y_c, abs(x_pos) - x_O, 3), numpy.uint8), canva))
                            alpha = numpy.hstack((numpy.zeros((y_c, abs(x_pos) - x_O, 1), numpy.uint16), alpha))
                            x_O = abs(x_pos) 

                        y_c, x_c, ch_c = canva.shape

                        #uzupełnianie pionu
                        if y_pos < 0  and abs(y_pos) > y_O:
                            "Pionowe przesuniecie w gore"
                            canva = numpy.vstack((numpy.zeros((abs(y_pos)-y_O, x_c, 3), numpy.uint8), canva))
                            alpha = numpy.vstack((numpy.zeros((abs(y_pos)-y_O, x_c, 1), numpy.uint16), alpha))
                            y_O = abs(y_pos)
                            # alpha = numpy.vstack((np.zeros((abs(y_pos)-y_O, x_c, 1),np.uint8), alpha))
                        if y_pos > 0  and y_O+y_pos+y_1>y_c:
                            "Pionowe przesuniecie w dol"
                            canva = numpy.vstack((canva, numpy.zeros((y_O+y_pos+y_1 - y_c, x_c, 3), numpy.uint8)))
                            alpha = numpy.vstack((alpha, numpy.zeros((y_O+y_pos+y_1 - y_c, x_c, 1), numpy.uint16)))

                        "obliczenie wspolczynnika, zsumowanie klatki i canvy, i inkrementacja wartosci alpha"
                        lvl = 1/(alpha[y_pos+y_O : y_pos+y_O+y_1, x_pos+x_O : x_pos+x_O+x_1] +1)
                        canva[y_pos+y_O : y_pos+y_O+y_1, x_pos+x_O : x_pos+x_O+x_1] = ((1-lvl)*canva[y_pos+y_O : y_pos+y_O+y_1, x_pos+x_O : x_pos+x_O+x_1]) + (lvl*input_data['color'])
                        alpha[y_pos+y_O : y_pos+y_O+y_1, x_pos+x_O : x_pos+x_O+x_1] += 1
                else:
                    "moze potem sie przyda"
                    pass

                output_stream.emit(output_data)
            output_data['object_photo'] = canva
            output_stream.emit(output_data)
                    
                    


                
                


            
                    
                    


                    

                             
         

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()