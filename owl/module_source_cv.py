import os
import sys
import json
import logging
import cv2
import redis
import task
import stream_video
import stream_data
import module_base

class Module(module_base.Module):

    def streams_init(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        output_task_data = {}

        cap = cv2.VideoCapture(self.params.get('device', 0))
        output_task_data['source_name'] = self.params.get('source_name',self.params.get('device', "unknown"))
        with self.task_emit(output_task_data) as output_stream:
            ret,frame = cap.read()
            while(not frame is None): 
                data = {
                    'color' : frame,
                    'metrics' : {"name": "asddas"}
                }
                output_stream.emit(data)
                ret,frame = cap.read() 
        cap.release()
        logging.info("end of input stream")


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()