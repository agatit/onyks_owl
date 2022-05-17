import torch
import numpy as np
import cv2 as cv
from time  import time


class Object_detection:

    def __init__(self, path, output, model_path):
        self.path = path
        self.model_path = model_path
        self.model = self.load_model()
        self.classes = self.model.names
        self.output = output
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('\n Used device:', self.device)

    def get_video_from_path(self):
        return cv.VideoCapture(self.path)
    
    def load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path = self.model_path)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:,:-1]
        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        labels, cord =results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                colour = (0, 255, 0)
                cv.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                cv.putText(frame, self.class_to_label(labels[i]), (x1,y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, colour, 2)
            
        return frame

    def __call__(self):
        player = self.get_video_from_path()
        assert player.isOpened()       #better if, do the program if the video is opened
        x_shape = int(player.get(cv.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv.VideoWriter_fourcc(*"MJPG")
        out = cv.VideoWriter(self.output, four_cc, 20, (x_shape, y_shape))          #parameters: file_mane, int fourcc, fps, frameSize, bool_is_colour = True
        while(1):
            start_time = time()
            ret,frame = player.read()
            if not ret:
                break
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            end_time = time()
            fps = 1/np.round(end_time - start_time, 3)
            print(f"FPS: {fps}")
            out.write(frame)


detection = Object_detection("/home/mbak/Realistic_contener_photos/14.58.00-15.06.00[R][0@0][0].mp4","yolo_detection_3_result.avi","/home/mbak/Yolo5/yolov5/runs/train/exp10/weights/best.pt")
detection()