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

        # dodać mapowanie strumieni !!!

    def task_process(self, input_task_data, input_stream):
        frame_no = 0
        for input_data in input_stream:
            if frame_no == 0:
                self.task_producers = []
                for oq in self.config.get('output_queues', []):
                    producers = {name: output_class for name, output_class in self.output_classes.items()}
                    self.task_producers.append(task.Producer(self.redis, oq, producers, self.expire_time))
                output_task_data = input_task_data
                for producer in self.task_producers:
                    output_stream = producer.task_emit(output_task_data)
                detection = False
            output_data = input_data
            output_stream.emit(output_data)
            frame_no += 1

        output_stream.end()
        logging.info("input task done")

    def task_emit(self, output_task_data):
        if not self.task_producer is None:
            output_stream = self.task_producer.emit(output_task_data)
            return output_stream
        else:
            raise Exception("No task output queue defined")

    def run(self):
        while not self.terminate:
            self.runOnce()
            time.sleep(1)


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
