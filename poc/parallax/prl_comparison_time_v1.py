import time
import os
import cv2
import numpy as np

def getDispNorm(imgL, imgR):
    disp = stereo.compute(imgL, imgR).astype(np.float32)
    return disp

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')

windowNameD = 'Concatenate'
windowSize = (640, 480)
# resizeSize = (1280, 720)
resizeSize = (640, 360)

cv2.namedWindow(windowNameD, cv2.WINDOW_FREERATIO)
cv2.resizeWindow(windowNameD, 1920, 1080)

cap = cv2.VideoCapture(v_name)


# Setting parameters for StereoSGBM algorithm
minDisparity = 0;
numDisparities = 64;
blockSize = 8;
disp12MaxDiff = 1;
uniquenessRatio = 10;
speckleWindowSize = 10;
speckleRange = 8;

# Creating an object of StereoSGBM algorithm
stereo = cv2.StereoSGBM_create(minDisparity = minDisparity,
        numDisparities = numDisparities,
        blockSize = blockSize,
        disp12MaxDiff = disp12MaxDiff,
        uniquenessRatio = uniquenessRatio,
        speckleWindowSize = speckleWindowSize,
        speckleRange = speckleRange
    )

start_time = time.time()
ret, imgR = cap.read() 

imgL = imgR
ret, imgR = cap.read() 

while ret:
    imgL = cv2.resize(imgL, windowSize)
    imgR = cv2.resize(imgR, windowSize)
    
    dispNorm = getDispNorm(imgL, imgR)
    cv2.imshow(windowNameD, dispNorm)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    imgL = imgR
    ret, imgR = cap.read()

print("--- %s seconds ---" % (time.time() - start_time))