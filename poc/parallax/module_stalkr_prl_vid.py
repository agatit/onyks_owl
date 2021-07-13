import os
import cv2
import numpy as np

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')


windowNameA = 'Left/prev frame'
windowNameB = 'Right/next frame'
windowNameC = 'Disparity'
windowNameD = 'Concatenate'
windowSize = (640, 480)

# cv2.namedWindow(windowNameA, cv2.WINDOW_FREERATIO)
# cv2.resizeWindow(windowNameA, windowSize)

# cv2.namedWindow(windowNameB, cv2.WINDOW_FREERATIO)
# cv2.resizeWindow(windowNameB, windowSize)

# cv2.namedWindow(windowNameC, cv2.WINDOW_FREERATIO)
# cv2.resizeWindow(windowNameC, windowSize)

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


ret, imgR = cap.read() 

imgL = imgR
ret, imgR = cap.read() 




while ret:
    imgL = cv2.resize(imgL, windowSize)
    imgR = cv2.resize(imgR, windowSize)
    # Calculating disparith using the StereoSGBM algorithm
    disp = stereo.compute(imgL, imgR).astype(np.float32)
    disp = cv2.normalize(disp,0,255,cv2.NORM_MINMAX)

    # cv2.imshow(windowNameA, imgL)
    # cv2.imshow(windowNameB, imgR)
    # cv2.imshow(windowNameC, disp)
    

    disp = stereo.compute(imgL, imgR).astype(np.float32)
    disp = cv2.normalize(disp,0,255,cv2.NORM_MINMAX)

    # preconc = np.concatenate((imgL, imgR), axis = 1)
    disp2 = np.dstack((disp, disp, disp))
    disp3 = cv2.normalize(disp2, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # cv2.imshow(windowNameC, disp3)
    # conc = np.concatenate((preconc, disp3), axis = 0)
    preconc = np.concatenate((imgL, imgR), axis = 1)
    conc = np.concatenate((preconc, np.zeros_like(preconc)), axis = 0)
    conc[windowSize[1]:,int(windowSize[0]/2):int(windowSize[0]/2+windowSize[0])] = disp3
    cv2.imshow(windowNameD, conc)

    imgL = imgR
    ret, imgR = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()