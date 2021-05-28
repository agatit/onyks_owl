import module_base
import sys
import stream_data
import stream_video
import cv2
import logging


class Module(module_base.Module):
    def __init__(self, argv):
        self.input_classes = {
            "dane": stream_data.Consumer
            #     "color": stream_video.Consumer,
            #     "metrics": stream_data.Consumer
        }
        self.output_classes = {}
        super().__init__(argv)

    def task_process(self, input_task_data, input_stream):
        """odczyt danych"""

        # with input_stream as inputs:
        for inputs in input_stream:
            logging.error("ak: received: " + inputs["dane"])
            # print(inputs['dane'])
        # logging.info("ak: received: " + input_task_data["dane"])
        # for input_data in input_stream:
        #     cv2.imshow(self.params.get('window_name', 'noname'), input_data['color'])
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
