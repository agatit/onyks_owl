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
    
    # def __init__(self):
    #     super(Module, self).__init__()
    
    @classmethod
    def get_config(cls):
        config = super(Module, cls).get_config()   
        config['params']['device'] = {'type': 'string|int', 'value': 0}
        config['input_classes'] = {}
        config['output_classes'] = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer
        }
        return config

    def task_process(self, input_task_data, input_stream):
        'przetwarzanie strumieni'
        # self.output_classes['color'] = 
        # self.output_classes['metrics'] = 
        os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

        output_task_data = {}
        filename = self.params['device']
        cap = cv2.VideoCapture(filename)
        try:
            output_task_data['source_name'] = self.params['device'] if self.params['device'] != 0 else "unknown" 
            with self.task_emit(output_task_data) as output_stream:
                ret,frame = cap.read()
                while(not frame is None): 
                    data = {
                        'color' : frame,
                        'metrics' : {"name": "asddas"}
                    }
                    output_stream.emit(data)
                    ret,frame = cap.read() 
            self.log_object.info("end of input stream")
        finally:
            cap.release()            


if __name__ == "__main__":
    module = Module.from_cmd(sys.argv)
    module.run()