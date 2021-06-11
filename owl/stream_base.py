# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strumieni danych"""
import json

		

class Producer:
    def __init__(self, redis, stream_queue, expire_time=10):
        self.id = id
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time     
        self.refresh = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.end()

    def emit(self, data):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", data)
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)

    def end(self):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", b"")
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)


class Consumer:
    def __init__(self, redis, stream_queue, timeout=5):
        self.redis = redis
        self.stream_queue = stream_queue
        self.timeout = timeout     
        self.refresh = 1

    def __iter__(self):
        return self

    def __next__(self):        
        resp = self.redis.blpop(f"owl:stream_queue:{self.stream_queue}", self.timeout)
        if resp is None:
            raise StopIteration

        data_bytes = resp[1]        

        if data_bytes != b"":
            return data_bytes
        else:
            raise StopIteration            


