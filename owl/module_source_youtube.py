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
import pafy
import time



class Module(module_base.Module):

    def streams_init(self): 
        self.input_classes = {}
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }

        video = pafy.new(self.params['url'])
        for v in video.allstreams:
            print(v)

        if "stream" in self.params:
            self.stream = next(v for v in video.allstreams if str(v) == self.params["stream"])
        else:
            self.stream = video.getbest(preftype="mp4")


    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'

        # cap = cv2.VideoCapture(self.params.get('device', 0))
        cap = cv2.VideoCapture(self.stream.url)
        with self.task_emit({}) as output_stream:
            ret,frame = cap.read()
            while(not frame is None): 
                data = {
                    'color' : frame,
                    'metrics' : {"name": "asddas"}
                }
                output_stream.emit(data)
                #time.sleep(0.5) 
                ret,frame = cap.read()                 
        cap.release()
        logging.info("end of input stream")


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()