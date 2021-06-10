# -*- coding: utf-8 -*-
# Created by: Marcin Bak
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł sprawdzajacy obecnosc pociagu"""

import os
import sys
import json
import logging
import cv2
import redis
import task
import stream_video
import stream_data
import module_base

hopefully_train_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")


class Module(module_base.Module):
    def __init__(self, argv): 
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }   
        self.output_classes = {
            "train_check": stream_data.Producer ,
            "train_pos": stream_data.Producer

        }
        super().__init__(argv)  

    def task_process(self, input_task_data, input_stream ):
        "sprawdzanie czy jest pociag"
        
        Factor = self.params.get("factor")
        neighbour = self.params.get("sasiad")

        with self.task_emit({}) as output_stream:
            
            for input_data in input_stream:
                train_check = False
                gray = cv2.cvtColor(input_data, cv2.COLOR_BGRA2GRAY)
                object = hopefully_train_cascade.detectMultiScale(gray, Factor,neighbour)
                for (x,y,w,h) in object: 
                    train_check = True  
                    # to_be_send = { "train_check": train_check, "train_pos": (x,y,w,h)}
                    # output_stream.emit(to_be_send) 
                    cv2.rectangle(gray,(x, x+w), (y, y+h), (255,0,0), 5)
                    cv2.imshow("img", gray)                     
                

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()