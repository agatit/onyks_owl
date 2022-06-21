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

class Producer():
    """Producent zdarzeń. Tworzy zdarzenia i umieszcza je w kolejach (kilku), zarządza powiązanymi strumieniami"""

    def __init__(
            self,
            redis: redis.Redis,
            task_queue: str,
            streams_classes: dict,
            expire_time: int,
            queue_limit: int,
            timeout: int):
        self.redis = redis
        self.task_queue = task_queue
        self.streams_classes = streams_classes
        self.expire_time = expire_time
        self.timeout = timeout
        self.queue_limit = queue_limit          

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
            "stream_names" : task_stream_queues,
            "task_data": task_data
        }

        logging.info(f"task emited: {task}")

        self.redis.rpush(f"owl:task_queue:{self.task_queue}", json.dumps(task))
        self.redis.expire(f"owl:task_queue:{self.task_queue}", self.expire_time)
      
        return stream_composed.Producer(self.redis, streams_queues, self.streams_classes, self.expire_time, self.queue_limit, self.timeout)

class Consumer():
    """Konsument zdarzeń. Odczytuje zdarzenia z kojejki (jednej) i podłącza powiązane strumienie"""

    def __init__(
            self,
            redis: redis.Redis,
            task_queue: str,
            streams_classes: dict,
            timeout: int):
        self.redis = redis
        self.task_queue = task_queue
        self.streams_classes = streams_classes
        self.timeout = timeout


    def __iter__(self):
        return self

    def __next__(self) -> (dict, stream_composed.Consumer):      
        """odczytanie zdarzenia z kolejki i podłączenie powiązanych strumieni"""
        
        if self.task_queue != "":
            task_data = self.redis.blpop(f"owl:task_queue:{self.task_queue}", self.timeout)
            if not task_data is None:
                task_str = task_data[1]
                task = json.loads(task_str)
                logging.info(f"task received: {task}")
                return task['task_data'], stream_composed.Consumer(self.redis, task['stream_names'], self.streams_classes, self.timeout)
            else:
                return None, None
        else:
            return {}, stream_composed.Consumer(self.redis, {}, {}, self.timeout)