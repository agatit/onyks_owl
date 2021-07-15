import time
import os
import cv2
import numpy as np


v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')

windowSize = (640, 480)
# resizeSize = (1280, 720)
resizeSize = (640, 360)


cap = cv2.VideoCapture(v_name)

wsize = 7
max_disp = 160
wls_lambda = 8000
wls_sigma = 1.5

# wersja z StereoBM
left_matcher = cv2.StereoBM_create()
wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher)
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

start_time = time.time()
ret, imgR = cap.read() 

imgL = imgR
ret, imgR = cap.read() 

while ret:
    imgL = cv2.resize(imgL, resizeSize)
    imgR = cv2.resize(imgR, resizeSize)

    left_for_matcher = cv2.cvtColor(imgL,  cv2.COLOR_BGR2GRAY)
    right_for_matcher = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    left_disp = left_matcher.compute(left_for_matcher, right_for_matcher)
    right_disp = right_matcher.compute(right_for_matcher, left_for_matcher)

    wls_filter.setLambda(wls_lambda)
    wls_filter.setSigmaColor(wls_sigma)
    filtered_disp = wls_filter.filter(left_disp,imgL,disparity_map_right=right_disp)

    vis = cv2.ximgproc.getDisparityVis(filtered_disp)

    cv2.imshow("vis",vis)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    imgL = imgR
    ret, imgR = cap.read() 
    
print("--- %s seconds ---" % (time.time() - start_time))