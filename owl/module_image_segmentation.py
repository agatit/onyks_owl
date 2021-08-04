import os
import numpy as np
import cv2
import tensorflow as tf
from operator import mod
import logging
import sys
import time
import stream_composed
import stream_video
import stream_data
import module_base
import sys


from models.modelSegmentation import build_model, iou

# Moduł dokonujący segmentacji wagonów:
class Module(module_base.Module):
    def streams_init(self):
        self.input_classes = {
            "color" : stream_video.Consumer,
            "metrics" : stream_data.Consumer
        }
        self.output_classes = {
            "color" : stream_video.Producer,
            "metrics" : stream_data.Producer,
            "mask" : stream_video.Producer
        }
        #Tworzenie modelu i kopiowanie wag z wcześniej nauczonego modelu
        lr = 1e-4
        self.model = build_model()
        opt = tf.keras.optimizers.Adam(lr)
        metrics = ["acc", tf.keras.metrics.Recall(), tf.keras.metrics.Precision(), iou]
        self.model.compile(loss="binary_crossentropy", optimizer=opt, metrics=metrics)
        modelPath = self.params.get('model_path', ".")
        self.model.load_weights(modelPath)

    def mask_parse(self, mask):
        mask = np.squeeze(mask)
        mask = [mask, mask, mask]
        mask = np.transpose(mask, (1, 2, 0))
        return mask

    def frame_prepare(self, frame):
        frame = cv2.resize(frame, (256, 256))
        frame = frame/255.0
        return frame


    def task_process(self, input_task_data, input_stream):

        output_task_data = input_task_data
        output_stream = None  
        output_data = {}
                 
        with self.task_emit({}) as output_stream:
            for input_data in input_stream:
                
                output_data = input_data
                frame = input_data['color']
                frame = self.frame_prepare(frame)
                begin = time.time()
                pred = self.model.predict(np.expand_dims(frame, axis=0))[0] > 0.5
                finalMask = self.mask_parse(pred) * 255.0   #maska wynikowa
                logging.debug(f"Prediction time: {time.time() - begin}")
                output_data['mask'] = finalMask
                output_stream.emit(output_data)
                
        logging.debug('Module stop')

if __name__ == "__main__":
    module = Module(sys.argv)
    module.run()
