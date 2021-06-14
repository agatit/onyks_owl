# -*- coding: utf-8 -*-
# Created by: Hubert Kołodziejski
# Maitained by: Hubert Kołodziejski
# Created on: python 3.8.7
"""Moduł obsługujący strumienie danych"""
import stream_base
import json
	

class Producer(stream_base.Producer):

    def emit(self, data):
        data_bytes = json.dumps(data)
        super().emit(data_bytes)


class Consumer(stream_base.Consumer):

    def __next__(self):        
        data_bytes = super().__next__()
        return json.loads(data_bytes)
