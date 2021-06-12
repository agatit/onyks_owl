# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strunieni video"""
import stream_base
import cv2 as cv
import io
from PIL import Image
import numpy as np
import time
		

class Producer(stream_base.Producer):
    def __init__(self, redis, stream_queue, expire_time=120, queue_limit=0, timeout=120):
        super().__init__(redis, stream_queue, expire_time, queue_limit, timeout)
        self.encoding_time = 0

    def emit(self, image):
        start = time.time()
        img_pil = Image.fromarray(image)
        with io.BytesIO() as b:
            img_pil.save(b,"JPEG")
            b.seek(0)            
            self.encoding_time = self.encoding_time * 0.99 + (time.time() - start) * 0.01
            print(f"kodowanie: {self.encoding_time:.5f} zapis: {self.writing_time:.5f}")
            super().emit(b.read())


class Consumer(stream_base.Consumer):
    def __init__(self, redis, stream_queue, timeout=120):
        super().__init__(redis, stream_queue, timeout)
        self.decoding_time = 0

    def __next__(self):              
        img_bytes = super().__next__()
        start = time.time() 
        b = io.BytesIO(img_bytes)
        img_pil = Image.open(b)
        result =  np.asarray(img_pil)
        self.decoding_time = self.decoding_time * 0.99 + (time.time() - start) * 0.01
        print(f"odkodowywanie: {self.decoding_time:.5f}")
        return result