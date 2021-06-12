# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strunieni video"""
import stream_base
import os
import cv2 as cv
import turbojpeg
# import io
# from PIL import Image
# import blosc
import numpy as np
import time
		
jpeg = turbojpeg.TurboJPEG()

class Producer(stream_base.Producer):
    def __init__(self, redis, stream_queue, expire_time=120, queue_limit=0, timeout=120):
        super().__init__(redis, stream_queue, expire_time, queue_limit, timeout)
        self.encoding_time = 0

    def emit(self, image):
        start = time.time()

        #opencv
        # _,img_np = cv.imencode(".BMP", image)
        # img_bytes = img_np.tobytes()

        # pillow-simd
        # img_pil = Image.fromarray(image)
        # with io.BytesIO() as b:
        #     img_pil.save(b,"JPEG")
        #     b.seek(0)    
        #     img_bytes = b.read()    
        
        #turbojpeg
        img_bytes = jpeg.encode(image, quality=80)        

        # blosc lz4
        # img_bytes = blosc.pack_array(image, cname='lz4')

        # numpy/pickle
        # with io.BytesIO() as b:
        #     np.save(b, image, allow_pickle=True)   
        #     b.seek(0) 
        #     img_bytes = b.read()      

        self.encoding_time = self.encoding_time * 0.99 + (time.time() - start) * 0.01
        print(f"kodowanie: {self.encoding_time:.5f} zapis: {self.writing_time:.5f}")
        super().emit(img_bytes)


class Consumer(stream_base.Consumer):
    def __init__(self, redis, stream_queue, timeout=120):
        super().__init__(redis, stream_queue, timeout)
        self.decoding_time = 0

    def __next__(self):              
        img_bytes = super().__next__()
        start = time.time() 

        #opencv
        # img_np = np.frombuffer(img_bytes, np.uint8)
        # result = cv.imdecode(img_np, cv.IMREAD_COLOR)

        # pillow-simd
        # b = io.BytesIO(img_bytes)
        # img_pil = Image.open(b)
        # result =  np.asarray(img_pil)

        # turgojpeg
        result = jpeg.decode(img_bytes)

        # blosc lz4
        # result = blosc.unpack_array(img_bytes)

        # numpy/pickle
        # b = io.BytesIO(img_bytes)
        # result = np.load(b, allow_pickle=True)

        self.decoding_time = self.decoding_time * 0.99 + (time.time() - start) * 0.01
        print(f"odkodowywanie: {self.decoding_time:.5f}")
        return result