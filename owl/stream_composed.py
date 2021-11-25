# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący połączone strumienie redis"""
import redis


class Producer():

    def __init__(
            self,
            redis: redis.Redis,
            streams_queues:[],
            streams_classes:[],
            queue_limit:int,
            expire_time:int,            
            timeout:int):
        self.streams = {}
        self.streams_queues = streams_queues
        self.streams_classes = streams_classes
        for stream_name, stream_class in streams_classes.items():
            self.streams[stream_name] = stream_class(redis, streams_queues[stream_name], queue_limit, expire_time, timeout)

    def __enter__(self):
        for p in self.streams.values():
            p.__enter__()
        return self

    def __exit__(self, type, value, tb):
        for p in self.streams.values():
            p.__exit__(type, value, tb)

    def emit(self, data):
        for stream_name, stream_data in data.items():
            self.streams[stream_name].emit(stream_data)

    def end(self):
        for p in self.streams.values():
            p.end()


class Consumer():

    def __init__(
            self,
            redis: redis.Redis,
            streams_queues:[],
            streams_classes:[],
            expire_time:int,
            timeout:int):       
        self.streams_queues = streams_queues
        self.streams_classes = streams_classes
        self.streams = {}
        for stream_name, stream_class in streams_classes.items():
            self.streams[stream_name] = stream_class(redis, f"{streams_queues[stream_name]}", expire_time, timeout)

    def __iter__(self):
        return self

    def __next__(self):  
        res = {}
        stop = False

        for stream_name, stream in self.streams.items():
            try:
                res[stream_name] = stream.__next__()
            except StopIteration:
                stop = True

        if stop:
            raise StopIteration

        return res


