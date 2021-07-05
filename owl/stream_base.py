# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strumieni danych"""
import json
import time
import redis
import logging

		

class Producer:
    def __init__(
            self,
            redis: redis.Redis,
            stream_queue: str,
            expire_time:int,
            queue_limit:int,
            timeout:int):
        self.id = id
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time
        self.timeout = timeout
        self.queue_limit = queue_limit  
        self.queue_space = queue_limit 
        self.refresh = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.end()

    def emit(self, data):
        end_time = time.time() + self.timeout
        while self.queue_limit > 0 and self.queue_space <= 0:  
            len = self.redis.llen(f"owl:stream_queue:{self.stream_queue}")
            self.queue_space = self.queue_limit - len
            if self.queue_space <= 0:
                time.sleep(0.1)        
            if time.time() > end_time:
                raise TimeoutError("Output stream queue is full")
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", data)
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)
        self.queue_space -= 1

    def end(self):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", b"")
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)


class Consumer:
    def __init__(
            self,
            redis: redis.Redis,
            stream_queue: str,
            timeout:int):
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


