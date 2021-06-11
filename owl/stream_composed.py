# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący połączone strumienie redis"""

class Producer():

    def __init__(self, redis, streams_queues, streams_classes, expire_time=120, queue_limit=0, timeout=120):
        self.streams = {}
        for stream_name, stream_class in streams_classes.items():
            self.streams[stream_name] = stream_class(redis, streams_queues[stream_name], expire_time, queue_limit, timeout)

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

    def __init__(self, redis, stream_queues, streams_classes, timeout=5):
        self.streams = {}
        for stream_name, stream_class in streams_classes.items():
            self.streams[stream_name] = stream_class(redis, f"{stream_queues[stream_name]}", timeout)

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


