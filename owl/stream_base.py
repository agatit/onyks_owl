# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strumieni danych"""
import json
import time

		

class Producer:
    def __init__(self, redis, stream_queue, expire_time=120, queue_limit=0, timeout=120):
        self.id = id
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time
        self.timeout = timeout
        self.queue_limit = queue_limit  
        self.queue_space = queue_limit 
        self.refresh = 1
        self.writing_time = 0 #debug

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.end()

    def emit(self, data):
        end_time = time.time() + self.timeout        
        while self.queue_limit > 0 and self.queue_space <= 0:   
            self.queue_space = self.queue_limit - self.redis.llen("owl:stream_queue:{self.stream_queue}")           
            if time.time() > end_time:
                raise TimeoutError("Output stream queue is full") 
            time.sleep(1)
        start = time.time()
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", data)
        self.writing_time = self.writing_time*0.99 + (time.time()-start)*0.01
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)
        self.queue_space -= 1

    def end(self):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", b"")
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)


class Consumer:
    def __init__(self, redis, stream_queue, timeout=120):
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


