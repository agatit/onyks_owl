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

# DEFAULT_PATH_LOGS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"logs")
DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"..", "projects")
class Module:
    def __init__(self, argv):
        'Czytanie konfiguracji i inicjalizacja'
        # handler = logging.StreamHandler(sys.stdout)
        # loggging.addHandler(handler)
        self.terminate = False
        logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)])
        
        self.module_name = self.__module__
        if self.module_name == '__main__':
            filename = sys.modules[self.__module__].__file__
            self.module_name = os.path.splitext(os.path.basename(filename))[0]        
        
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
        # logging.StreamHandler(sys.stdout)
        try:
            # print(len(argv))
            if len(argv) > 1:
                # print(argv[1:])
                with open(argv[1], "rb") as f:
                    config_file = json.load(f)
                    name = self.module_name

                    self.config = config_file['modules'][name]
                    if self.config is None:
                        logging.info(f"config file: {argv[1]} do not contain section for {name}")    
                        exit()

                    logging.info(f"config file: {argv[1]} section {name}")
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
                logging.error("task_expire_time CANNOT be bigger than task_timeout")
                exit()

            if self.stream_expire_time > self.stream_timeout:
                logging.error("stream_expire_time CANNOT be bigger than stream_timeout")
                exit()                

            if self.task_expire_time > self.stream_expire_time:
                logging.error("task_expire_time CANNOT be bigger than stream_expire_time")
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
                self.stream_timeout)
            producers = {name : output_class for name, output_class in self.output_classes.items()} 
            self.task_producer = task.Producer(
                self.redis,
                self.config.get('output_queue',""),
                producers,
                self.stream_queue_limit, 
                self.task_expire_time,
                self.task_timeout, 
                self.stream_expire_time,
                self.stream_timeout)  

        except Exception as e:
            logging.error(f"{self.module_name}: {str(e)}\n\n{u''.join(traceback.format_tb(e.__traceback__))}\n")
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
                        logging.debug("Nothing in task queue")
        except Exception as e:
           logging.error(f"{self.module_name} runOnce error: {str(e)}\n{u''.join(traceback.format_tb(e.__traceback__))}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)   

    def get_config(self):
        return self.default_config

if __name__ == "__main__":
    print("Do not call base class!")

