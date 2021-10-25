# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący kolejki zdarzeń"""

import os
import time
import logging
import json
import sys
import redis
import task
import traceback
import stream_composed

DEFAULT_PATH_LOGS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"logs")

class Module:
    def __init__(self, argv):
        'Czytanie konfiguracji i inicjalizacja'
        self.terminate = False

        self.module_name = self.__module__
        if self.module_name == '__main__':
            filename = sys.modules[self.__module__].__file__
            self.module_name = os.path.splitext(os.path.basename(filename))[0]        
        
        # handler = logging.StreamHandler(sys.stdout)
        # print("argv: ", argv)
        try:
            self.instance_id = argv[2] # np. perspective_transform_01
            if self.instance_id is not None:
                # try:
                #     os.mkdir(log_dir)
                # except:
                #     pass
                # print("log_dir: ", log_dir)
                # log_dir = DEFAULT_PATH_LOGS + '_' + self.module_name + '.txt' # TODO ogarnąć to po ludzku
                log_dir = os.path.join(DEFAULT_PATH_LOGS, self.module_name + '_' + self.instance_id + '.txt')
                handler = logging.FileHandler(filename = log_dir, mode='w') # TODO zastanowić się czy mode='w' czy mode='a'
                formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
                handler.setFormatter(formatter)
                # logging.basicConfig(level=logging.DEBUG, handlers=[handler])
                self.log_object = logging.getLogger(name='logger4'+self.module_name)
                self.log_object.setLevel(logging.DEBUG)
                self.log_object.addHandler(handler)
                self.log_object.info(f"{self.module_name} started.")
            else:
                self.instance_id = None
                self.log_object = None
        except:
            self.instance_id = None
            self.log_object = None

        self.default_config = {
            'stream_queue_limit': ['int', 100],
            'task_expire_time': ['int', 10],
            'stream_expire_time': ['int', 10],
            'task_timeout': ['int', 10],
            'stream_timeout': ['int', 10],
            "params": ['parameters', {}],
            'input_queue': ['string', ""],
            'output_queue': ['string', ""],
        }
        try:
            # print(len(argv))
            if len(argv) > 1:
                # print(argv[1:])
                with open(argv[1], "rb") as f:
                    config_file = json.load(f)
                    name = self.module_name

                    self.config = config_file['modules'][name]
                    if self.config is None:
                        if self.instance_id is not None:
                            self.log_object.info(f"config file: {argv[1]} do not contain section for {name}")    
                        exit()

                    if self.instance_id is not None:
                        self.log_object.info(f"config file: {argv[1]} section {name}")
            else:
                print("Usage: module config_file.json [instance_name]")
                exit()  

            self.stream_queue_limit = self.config.get('stream_queue_limit', self.default_config['stream_queue_limit'][1])
            self.task_expire_time = self.config.get('task_expire_time', self.default_config['task_expire_time'][1])
            self.stream_expire_time = self.config.get('stream_expire_time', self.task_expire_time) # TODO ???
            self.task_timeout = self.config.get('task_timeout', self.stream_expire_time)            
            self.stream_timeout = self.config.get('stream_timeout', self.stream_expire_time)            
            self.params = self.config.get("params", self.default_config['params'][1])

            if self.task_expire_time > self.task_timeout:
                if self.instance_id:
                    self.log_object.error("task_expire_time CANNOT be bigger than task_timeout")
                exit()

            if self.stream_expire_time > self.stream_timeout:
                if self.instance_id:
                    self.log_object.error("stream_expire_time CANNOT be bigger than stream_timeout")
                exit()                

            if self.task_expire_time > self.stream_expire_time:
                if self.instance_id:
                    self.log_object.error("task_expire_time CANNOT be bigger than stream_expire_time")
                exit()                

            self.redis = redis.Redis()

            self.streams_init()
                               
            consumers = {name : input_class for name, input_class in self.input_classes.items()}        
            self.task_consumer = task.Consumer(
                self.redis,
                self.config.get('input_queue', ""),
                consumers,
                self.task_expire_time,
                self.task_timeout,
                self.stream_expire_time,
                self.stream_timeout,
                self.log_object)
            producers = {name : output_class for name, output_class in self.output_classes.items()} 
            self.task_producer = task.Producer(
                self.redis,
                self.config.get('output_queue',""),
                producers,
                self.stream_queue_limit, 
                self.task_expire_time,
                self.task_timeout, 
                self.stream_expire_time,
                self.stream_timeout,
                self.log_object)  

        except Exception as e:
            if self.instance_id:
                self.log_object.error(f"{self.module_name}: {str(e)}\n\n{u''.join(traceback.format_tb(e.__traceback__))}\n")
            self.terminate = True           


    def streams_init(self):
        self.input_classes = {}
        self.output_classes = {}


    def task_process(self, input_task_data: dict, input_stream: stream_composed.Consumer):
        pass


    def task_emit(self, output_task_data): 
        if not self.task_producer is None:       
            output_stream = self.task_producer.emit(output_task_data)
            return output_stream
        else:
            raise Exception("No task output queue defined")


    def runOnce(self):       
        try:
            with self.task_producer:
                for task_data, input_stream in self.task_consumer:
                    if not task_data is None:
                        task = {
                            "stream_names" : input_stream.streams_queues,
                            "task_data": task_data
                        }
                        self.redis.set(f"owl:module:{self.module_name}:task", json.dumps(task), ex=self.task_expire_time)
                        self.task_process(task_data, input_stream)                                
                    else:
                        self.log_object.debug("Nothing in task queue")
        except Exception as e:
            self.log_object.error(f"{self.module_name} runOnce error: {str(e)}\n{u''.join(traceback.format_tb(e.__traceback__))}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)   

    def get_config(self):
        return self.default_config

if __name__ == "__main__":
    print("Do not call base class!")

