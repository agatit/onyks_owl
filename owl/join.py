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
import module_base

class Module(module_base.Module):
    def __init__(self, config):
        'Czytanie konfiguracji i inicjalizacja'

        super().__init__(config)  

        consumers = {name : input_class for name, input_class in self.input_classes.items()}        
        self.task_consumer = task.Consumer(self.redis, self.config.get('input_queue', ""), consumers, self.timeout) 
        
        
        ###############################
        # buduje zadania i dodaje je kolejki do strumieni
        for q in self.task_queues:
            task_stream_queues = {}

            common_queue_name = uuid.uuid4().hex
            for sn in streams_queues.keys():
                stream_queue_name = f"{common_queue_name}.{sn}"
                task_stream_queues[sn] = stream_queue_name
                streams_queues[sn].append(stream_queue_name)

            task = {
                "stream_names" : task_stream_queues,
                "task_data": task_data
            }

            logging.info(f"task emited: {task}")

            self.redis.rpush(q, json.dumps(task))
            self.redis.expire(q, self.expire_time)
      
        return stream_composed.Producer(self.redis, streams_queues, self.streams_classes, self.expire_time * 2)             

        except Exception as e:
            logging.error(f"{self.module_name} init error: {str(e)}") 
        

    def task_process(self, input_task_data, input_stream ):                   
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
                        self.task_process(task_data, input_stream)                                
                    else:
                        logging.info("Nothing in task queue")
        except Exception as e:
            logging.error(f"{self.module_name} runOnce error: {str(e)}")


    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)   


if __name__ == "__main__":
    print("Do not call base class!")

