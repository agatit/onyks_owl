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

class Module:
    def __init__(self, argv):
        'Czytanie konfiguracji i inicjalizacja'
        self.terminate = False

        self.module_name = self.__module__
        if  self.module_name == '__main__':
            filename = sys.modules[self.__module__].__file__
            self.module_name = os.path.splitext(os.path.basename(filename))[0]        
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])
        logging.info(f"{self.module_name} started.")

        try:
            if len(argv) > 1:
                with open(argv[1], "rb") as f:
                    config_file = json.load(f)                    
                    if len(argv) > 2:
                        name = argv[2]
                    else:
                        name = self.module_name                    

                    self.config = config_file[name]
                    if self.config is None:
                        logging.info(f"config file: {argv[1]} do not contain section for {name}")    
                        exit()

                    logging.info(f"config file: {argv[1]} section {name}")
            else:
                print("Usage: module config_file.json [instance_name]")
                exit()  

            self.expire_time = self.config.get('expire_time', 120)
            self.timeout = self.config.get('timeout', 10)  
            self.stream_queue_limit = self.config.get('stream_queue_limit', 0)
            self.params = self.config.get("params", {})

            self.redis = redis.Redis()

            self.streams_init()
                               
            consumers = {name : input_class for name, input_class in self.input_classes.items()}        
            self.task_consumer = task.Consumer(self.redis, self.config.get('input_queue', ""), consumers, self.timeout)
            producers = {name : output_class for name, output_class in self.output_classes.items()} 
            self.task_producer = task.Producer(self.redis, self.config.get('output_queue',""), producers, self.expire_time, self.stream_queue_limit,  self.timeout)  

        except Exception as e:
            logging.error(f"{self.module_name}: {str(e)}\n\n{''.join(traceback.format_tb(e.__traceback__))}\n")
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
                        self.redis.set(f"owl:module:{self.module_name}:task", json.dumps(task), ex=self.expire_time)
                        self.task_process(task_data, input_stream)                                
                    else:
                        logging.info("Nothing in task queue")
        except Exception as e:
            logging.error(f"{self.module_name} runOnce error: {str(e)}\n{traceback.print_tb(e.__traceback__)}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)   


if __name__ == "__main__":
    print("Do not call base class!")

