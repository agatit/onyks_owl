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
    module_name = "module_base"
    log_object = None
    terminate = False
    instance_id = None
    
    def __init__(self, config, connector):

        self.build_config()
        self.config = config
        for k, v in config.items():
            setattr(self, k, v)

        self.connector = connector        

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

        self.setup()
                            
        consumers = {name : input_class for name, input_class in self.input_classes.items()}        
        self.task_consumer = task.Consumer(
            self.redis,
            self.config.get('input_queue', ""),
            consumers,
            self.task_expire_time,
            self.task_timeout,
            self.stream_expire_time,
            self.stream_timeout,
            log_object = self.log_object)
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
            log_object = self.log_object)  

    @classmethod
    def from_cmd(cls, argv):
        'Czytanie konfiguracji i inicjalizacja'
        self = None

        module_name = cls.__module__
        if module_name == '__main__':
            filename = sys.modules[cls.__module__].__file__
            module_name = os.path.splitext(os.path.basename(filename))[0]
        
        try:
            instance_id = argv[2] # np. perspective_transform_01
            if instance_id is not None:
                log_object = logging.getLogger(name='owl_' + instance_id + "_" + module_name)
                print('owl_' + instance_id + "_" + module_name)
                log_object.warning(f"{module_name} started.")
                print(f"{module_name} started.")
            else:
                instance_id = None
                log_object = None
        except:
            instance_id = None
            log_object = None

        try:
            if len(argv) > 1:
                with open(argv[1], "rb") as f:
                    config_file = json.load(f)                
                    #config = config_file['modules'][module_name]
                    config = config_file['modules'][module_name]
                    if config is None:
                        if instance_id is not None:
                            log_object.info(f"config file: {argv[1]} do not contain section for {module_name}")    
                        exit()

                    if instance_id is not None:
                        log_object.info(f"config file: {argv[1]} section {module_name}")

                    cls.log_object = log_object
                    self = cls(config, None) # TODO: obsłuzyć connector                                       
                    self.module_name = module_name
                    # self.log_object = log_object
                    self.terminate = False
            else:
                print("Usage: module config_file.json [instance_name]")
                exit()  

            ######

        except Exception as e:
            print(f"{module_name}: {str(e)}\n\n{u''.join(traceback.format_tb(e.__traceback__))}\n")
            log_object.error(f"{module_name}: {str(e)}\n\n{u''.join(traceback.format_tb(e.__traceback__))}\n")
        
        return self          

    @classmethod
    def from_dict(cls, instance_name, config):
        pass

    def setup(self):
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
            if self.log_object:
                self.log_object.error(f"{self.module_name} runOnce error: {str(e)}\n{u''.join(traceback.format_tb(e.__traceback__))}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)

    def build_config(self):
        # self.stream_queue_limit = self.config.get('stream_queue_limit', self.default_config['stream_queue_limit'][1])
        # self.task_expire_time = self.config.get('task_expire_time', self.default_config['task_expire_time'][1])
        # self.stream_expire_time = self.config.get('stream_expire_time', self.task_expire_time)
        # self.task_timeout = self.config.get('task_timeout', self.stream_expire_time)            
        # self.stream_timeout = self.config.get('stream_timeout', self.stream_expire_time)            
        # self.params = self.config.get("params", self.default_config['params'][1])        
        
        config = self.get_config()
        for k, v in config['params'].items():
            setattr(self, k, v['value'])

        self.input_classes = config['input_classes']
        self.output_classes = config['output_classes']            

    @classmethod
    def get_config(cls):
        config = {}
        config['params'] = {
            'stream_queue_limit': {'type': 'int', 'value': 100},
            'task_expire_time': {'type': 'int', 'value': 10},
            'stream_expire_time': {'type': 'int', 'value': 10},
            'task_timeout': {'type': 'int', 'value': 10},
            'stream_timeout': {'type': 'int', 'value': 10},
            'input_queue': {'type': 'string', 'value': ""},
            'output_queue': {'type': 'string', 'value': ""},
        }    
        config['input_classes'] = {}
        config['output_classes'] = {}        

        return config

if __name__ == "__main__":
    print("Do not call base class!")

