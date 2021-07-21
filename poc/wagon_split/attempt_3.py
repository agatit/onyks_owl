import cv2
import os
import numpy as np

cv2.namedWindow('Frame', cv2.WINDOW_FREERATIO)
cv2.namedWindow('FG Mask', cv2.WINDOW_FREERATIO)
# cv2.namedWindow('FG Masked', cv2.WINDOW_FREERATIO)
cv2.namedWindow('FG Mask Closed', cv2.WINDOW_FREERATIO)
v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39.mp4')


backSub = cv2.createBackgroundSubtractorMOG2()

capture = cv2.VideoCapture(v_name)
ret, frame = capture.read()
while ret:

    fgMask = backSub.apply(frame)
    
    
    cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv2.putText(frame, str(capture.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    kernel = np.ones((3,3),np.uint8)
    fgMaskClosed = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel, iterations=3)
    # fgMasked = np.copy(frame)
    # fgMasked[fgMask == 0] = 0
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fgMask)
    # cv2.imshow('FG Masked', fgMasked)
    cv2.imshow('FG Mask Closed', fgMaskClosed)
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    ret, frame = capture.read()