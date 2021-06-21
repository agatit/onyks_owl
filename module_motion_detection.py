from operator import mod
import numpy as np
import cv2
import sys
import redis
import json
import stream_composed
import module_base

# Moduł do detekcji pociągów:

class Module(module_base.Module):

    def fixColor(image):
        if(cv2.CAP_PROP_CONVERT_RGB):
            print("Conversion BGR_to_RGB done succesfully")
        return(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def fixGray(image):
        return(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    
    def task_process(self, input_video_stream):
        input_video_stream = cv2.VideoCapture(0)
        frameIds = input_video_stream.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=30) #default: size=30 
        frames = []
        
        for fid in frameIds[:10]:
            input_video_stream.set(cv2.CAP_PROP_POS_FRAMES, fid)
            print("CAP_PROP_POS_FRAMES", cv2.CAP_PROP_POS_FRAMES)
            ret, frame = input_video_stream.read()
            frames.append(frame)
        
        input_video_stream.release()
        
        medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)
        medianFrame = fixColor(medianFrame)
        print("medianFrame.size:", medianFrame.shape)

        avgFrame = np.average(frames[:10], axis=1).astype(dtype=np.uint8)
        avgFrame = fixColor(avgFrame)
        print("avgFrame.size:", avgFrame.shape)
        
        sample_frame=frames[0]
        sample_frame = fixColor(sample_frame)
        print("sample_frame.size:", sample_frame.shape)
        
        grayMedianFrame = 
`       plt.imshow(fixColor(grayMedianFrame)
        print("grayMedianFrame.size:", grayMedianFrame.shape)
        return