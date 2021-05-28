# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strunieni video"""
import cv2 as cv
import numpy as np


class Producer():

    def __init__(self, redis, stream_queue, expire_time=30):
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time
        self.refresh = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.end()

    def emit(self, image):
        _, img_np = cv.imencode(".BMP", image)
        img_bytes = img_np.tobytes()
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", img_bytes)
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)

    def end(self):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", b"")
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)


class Consumer():

    def __init__(self, redis, stream_queue, timeout=5):
        self.redis = redis
        self.stream_queue = stream_queue
        self.refresh = 1
        self.timeout = timeout

    def __iter__(self):
        return self

    def __next__(self):
        resp = self.redis.blpop(f"owl:stream_queue:{self.stream_queue}", self.timeout)
        if resp is None:
            raise StopIteration

        img_bytes = resp[1]

        if img_bytes != b"":
            img_np = np.frombuffer(img_bytes, np.uint8)
            return cv.imdecode(img_np, cv.IMREAD_COLOR)
        else:
            raise StopIteration
