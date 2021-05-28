import sys
import module_base
import stream_video
import stream_data
import cv2
import logging
import numpy as np


class Module(module_base.Module):
    def __init__(self, config):
        self.input_classes = {
            "previous_frame": stream_video.Producer,
            "current_frame": stream_video.Producer,
            "content": stream_data.Producer  # False == (previous == current); True == (previous != current)
        }
        self.output_classes = {
            # "wideo": stream_video.Producer,
            # "dane": stream_data.Producer
        }
        super().__init__(config)

    def task_process(self, input_task_data, input_stream):

        if input_stream['content']:
            cv2.imshow(self.params.get('window_name', 'noname'), input_stream['previous_frame'])

        for input_data in input_stream:
            cv2.imshow(self.params.get('window_name', 'noname'), input_data['current_frame'])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == '__main__':
    module = Module(sys.argv)
    module.run()
