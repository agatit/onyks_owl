import sys
import module_base
import stream_video
import stream_data
import cv2
import logging


class Module(module_base.Module):
    def __init__(self, config):
        self.input_classes = {}
        self.output_classes = {
            # "wideo": stream_video.Producer,
            "dane": stream_data.Producer
        }
        super().__init__(config)

    def task_process(self, input_task_data, input_stream):
        # cv2.VideoCapture(self.params.get("device"))
        # print(self.params.get("device"), 0)
        # print("ok")
        logging.info("ak: task process starts")
        with self.task_emit({}) as output_stream:
            logging.info("ak: inside")
            dane = {
                "dane": self.params.get('device')
            }
            output_stream.emit(dane)
            logging.info("ak: task ends...")


if __name__ == '__main__':
    module = Module(sys.argv)
    module.run()
