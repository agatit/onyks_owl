#importing needed modules:
from operator import countOf, mod
from typing import Counter
import numpy as np
import cv2
import time

video_stream = cv2.VideoCapture("D:\Agat_IT\onyks_owl-main\onyks_owl-main\owl\out_2_10.mp4")
last_frame = None
grabbed, frame = video_stream.read()
frame_buffer = []
buffer_size = 25
compared_value = 150000
frame_counter = 0
state = 0
last_state = 0
print("grabbed:", grabbed)
while grabbed:
    period = time.time()
    if len(frame_buffer) > 9:
        dframe = cv2.absdiff(frame, frame_buffer[-5])
        gdframe = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
        ret, bwframe = cv2.threshold(gdframe,10,255,cv2.THRESH_BINARY)
        pixel_count = cv2.countNonZero(bwframe)
        
        #wybieranie na którym torze jest większy ruch:
        r, h, c, w = 600, 90, 230, 480
        track_window = (c, r, w, h)
        
        # set up the ROI for tracking
        roi = bwframe[r:r + h, c:c + w]
        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        
        ret, frame = video_stream.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
            # Draw it on image
            x, y, w, h = track_window
            cv2.rectangle(bwframe, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if cv2.waitKey(1) == ord('q'):
                break
        
        if pixel_count > compared_value: #detection is done
            state = 1
            print("state:", bool(state))
        else: #detection is not done
            state = 0
            print("state:", bool(state))
        if state == 1 or frame_counter < buffer_size:
            print("last_state_in_loop:", last_state)
            if state == 1 and last_state == 0:
                print("Tu ma być task")
                
            if state == 0:
                frame_counter += 1
                if frame_counter > buffer_size:
                    print("wywołanie end-a")
            else:
                frame_counter = 0
                
            cv2.imshow("bwframe:", bwframe)
            if cv2.waitKey(1) == ord('q'):
                break
    last_state = state
    print("last_state:", last_state)
        
    frame_buffer.append(frame)
    if len(frame_buffer) > buffer_size:
        frame_buffer.pop(0)
    grabbed, frame = video_stream.read()
    
video_stream.release()

