# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący kolejki zdarzeń"""

import json
import uuid
import logging
import redis
import stream_composed
from typing import Tuple


class Producer():
    """Producent zdarzeń. Tworzy zdarzenia i umieszcza je w kolejach (kilku), zarządza powiązanymi strumieniami"""

    def __init__(
            self,
            redis: redis.Redis,
            task_queue: str,
            streams_classes: dict,
            queue_limit: int,            
            task_expire_time: int,
            task_timeout: int,
            stream_expire_time: int,                        
            stream_timeout: int,
            log_object):

        self.redis = redis
        self.task_queue = task_queue
        self.streams_classes = streams_classes
        self.queue_limit = queue_limit

        self.task_expire_time = task_expire_time
        self.task_timeout = task_timeout
        self.stream_expire_time = stream_expire_time
        self.stream_timeout = stream_timeout
        self.log_object = log_object

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def emit(self, task_data: dict = {}) -> stream_composed.Producer:
        """umieszczenie zdarzenia w kolejce wyjściowej i utworzenie powiązanych strumieni"""

        streams_queues = {}

        # buduje liste strumieni z pustymi tablicami kolejki
        for sd in self.streams_classes:
            streams_queues[sd] = []

        # buduje zadania i dodaje je kolejki do strumieni
        task_stream_queues = {}

        common_queue_name = uuid.uuid4().hex
        for sn in streams_queues.keys():
            stream_queue_name = f"{self.task_queue}:{common_queue_name}:{sn}"
            task_stream_queues[sn] = stream_queue_name
            streams_queues[sn] = stream_queue_name

        task = {
            "stream_names": task_stream_queues,
            "task_data": task_data
        }

        self.log_object.info(f"task emited: {task}")

        p = self.redis.pipeline()  
        p.rpush(f"owl:task_queue:{self.task_queue}", json.dumps(task))
        p.expire(f"owl:task_queue:{self.task_queue}", self.task_expire_time)
        p.execute()          
      
        return stream_composed.Producer(
            self.redis,
            streams_queues,
            self.streams_classes,
            self.queue_limit,
            self.stream_expire_time,            
            self.stream_timeout,
            self.log_object)


class Consumer():
    """Konsument zdarzeń. Odczytuje zdarzenia z kojejki (jednej) i podłącza powiązane strumienie"""

    def __init__(
            self,
            redis: redis.Redis,
            task_queue: str,
            streams_classes: dict,            
            task_expire_time:int,
            task_timeout: int,
            stream_expire_time:int,
            stream_timeout: int,
            log_object):
        self.redis = redis
        self.task_queue = task_queue
        self.streams_classes = streams_classes
        self.task_expire_time = task_expire_time
        self.task_timeout = task_timeout
        self.stream_expire_time = stream_expire_time
        self.stream_timeout = stream_timeout
        self.log_object = log_object
    def __iter__(self):
        return self

    def __next__(self) -> Tuple[dict, stream_composed.Consumer]:
        """odczytanie zdarzenia z kolejki i podłączenie powiązanych strumieni"""

        if self.task_queue != "":
            task_data = self.redis.blpop(f"owl:task_queue:{self.task_queue}", self.task_timeout)
            if not task_data is None:
                task_str = task_data[1]
                task = json.loads(task_str)
                self.log_object.info(f"task received: {task}")
                return task['task_data'], stream_composed.Consumer(
                    self.redis, task['stream_names'],
                    self.streams_classes,
                    self.stream_expire_time,
                    self.stream_timeout,
                    self.log_object)
            else:
                return None, None
        else:
            return {}, stream_composed.Consumer(self.redis, {}, {}, self.stream_expire_time, self.stream_timeout, self.log_object)
