import sys
import module_base
import stream_video
import stream_data
import cv2
import logging
import numpy as np


class Module(module_base.Module):
    def __init__(self, config):
        self.input_classes = {}
        self.output_classes = {
            # "wideo": stream_video.Producer,
            # "dane": stream_data.Producer
            "previous_frame": stream_video.Producer,
            "current_frame": stream_video.Producer,
            "content": stream_data.Producer  # False == (previous == current); True == (previous != current)
        }
        super().__init__(config)

    def task_process(self, input_task_data, input_stream):
        cap = cv2.VideoCapture(self.params.get['file_source'])

        while True:
            with self.task_emit({}) as output_stream:
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    # break
                    break

                # send previous frame
                to_be_send = {
                    "previous_frame": frame,
                    "content": False
                    # "current_frame": stream_video.Producer
                }

                # output_stream.emit(to_be_send)

                while cap.isOpened():
                    ret, frame = cap.read()
                    # if frame is read correctly ret is True
                    if not ret:
                        logging.info("Can't receive frame (stream end?). previous_frame == current frame")
                        to_be_send['current_frame'] = to_be_send['previous_frame']  # the same frame
                        output_stream.emit(to_be_send)
                        break

                    #     send current frame
                    to_be_send['current_frame'] = frame
                    to_be_send['content'] = True
                    output_stream.emit(to_be_send)
                    to_be_send['previous_frame'] = frame


if __name__ == '__main__':
    module = Module(sys.argv)
    module.run()
