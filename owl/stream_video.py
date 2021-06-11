# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strunieni video"""
import stream_base
import cv2 as cv
import numpy as np
		

class Producer(stream_base.Producer):

    def emit(self, image):
        _,img_np = cv.imencode(".BMP", image)
        img_bytes = img_np.tobytes()
        super().emit(img_bytes)


class Consumer(stream_base.Consumer):

    def __next__(self):       
        img_bytes = super().__next__()
        img_np = np.frombuffer(img_bytes, np.uint8)
        return cv.imdecode(img_np, cv.IMREAD_COLOR)