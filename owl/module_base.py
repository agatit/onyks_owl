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
import connector_base

DEFAULT_PATH_LOGS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"logs")

class Module:  
    module_name = "module_base"    
    terminate = False
    instance_id = None
    
    def __init__(self, config: dict, connector: connector_base.Connector, log_object = logging.Logger):

        self.log_object = log_object

        self.build_config(config)

        self.connector = connector   

        #TODO: budowanie interfejsów kolejek     

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

        #self.redis = redis.Redis("172.22.137.23", 6378)
        self.redis = redis.Redis("127.0.0.1", 6379)        
                            
        self.task_setup()
      
        self.task_consumer = task.Consumer(
            self.redis,            
            self.input_queues[0] if len(self.input_queues) > 0 else "",
            {name : input_class for name, input_class in self.input_classes.items()},
            self.task_expire_time,
            self.task_timeout,
            self.stream_expire_time,
            self.stream_timeout,
            log_object = self.log_object)

        self.task_producer = task.Producer(
            self.redis,
            self.output_queues[0] if len(self.output_queues) > 0 else "",
            {name : output_class for name, output_class in self.output_classes.items()},
            self.stream_queue_limit, 
            self.task_expire_time,
            self.task_timeout, 
            self.stream_expire_time,
            self.stream_timeout,
            log_object = self.log_object)  

    @classmethod
    def from_cmd(cls, argv: list[str]):    

        'Czytanie konfiguracji i inicjalizacja'
        self = None

        module_name = cls.__module__
        if module_name == '__main__':
            filename = sys.modules[cls.__module__].__file__
            module_name = os.path.splitext(os.path.basename(filename))[0]

        log_object = logging.getLogger()
        log_object.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - {module_name} - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log_object.addHandler(handler)              
        
        try:
            if len(argv) > 2:
                instance_id = argv[2] # np. perspective_transform_01
            else:
                instance_id = module_name
        except:
            instance_id = module_name

        try:
            if len(argv) > 1:
                with open(argv[1], "rb") as f:
                    config_file = json.load(f)                
                    config = config_file['modules'][instance_id]
                    if config is None:
                        log_object.info(f"config file: {argv[1]} do not contain section for {instance_id}")
                        exit()

                    log_object.info(f"config file: section {instance_id} read from {argv[1]}")

                    try:
                        self = cls(config, None, log_object) # TODO: obsłuzyć connector
                        self.module_name = module_name
                        self.terminate = False                        
                    except Exception as e:
                        log_object.info(str(e))

                    return self
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

    def task_setup(self):
        pass

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
        except TimeoutError as e:
            if self.log_object:
                self.log_object.error(f"{self.module_name} runOnce error: {str(e)}")
        except Exception as e:
            if self.log_object:
                self.log_object.error(f"{self.module_name} runOnce error: {str(e)}\n{u''.join(traceback.format_tb(e.__traceback__))}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)

    def build_config(self, config: dict):   
        ''' Fills configuration variables based on configuration and defualt values'''                           

        self.input_queues = config.get("input_queues", [])
        self.output_queues = config.get("output_queues", [])

        default_config = self.get_config()

        self.params = {}
        for k, v in default_config['params'].items():
            self.params[k] = v['value']
        for k, v in config['params'].items():
            self.params[k] = v

        self.input_classes = {}
        for k, v in default_config['input_classes'].items():
            self.input_classes[k] = v

        self.output_classes = {}
        for k, v in default_config['output_classes'].items():
            self.output_classes[k] = v

        # TODO: do przeniesienia do Queue
        self.stream_queue_limit = self.params['stream_queue_limit']
        self.task_expire_time = self.params['task_expire_time']
        self.stream_expire_time = self.params['stream_expire_time']
        self.task_timeout = self.params['task_timeout']
        self.stream_timeout = self.params['stream_timeout'] 

    @classmethod
    def get_config(cls):
        ''' Returns module configuration definition.'''

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
        config['input_classes'] = {} # Zawiera słownik klas - przy odczycie trzeba użyć __class__.__name__
        config['output_classes'] = {}        

        return config

if __name__ == "__main__":
    print("Do not call base class!")

