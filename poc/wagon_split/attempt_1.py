import cv2
import numpy as np
import os

windowName = 'Canny Edge Detection'
alpha_slider_max = 1000
trackbar1_name = 'threshold1'
threshold1_default = 200
threshold1_value = threshold1_default

trackbar2_name = 'threshold2'
threshold2_default = 200
threshold2_value = threshold2_default

def set_threshold1(value):
    global threshold1_value, threshold2_value 
    threshold1_value = cv2.getTrackbarPos(trackbar1_name,windowName)
    threshold2_value = cv2.getTrackbarPos(trackbar2_name,windowName)


cv2.namedWindow(windowName, cv2.WINDOW_FREERATIO)
cv2.createTrackbar(trackbar1_name, windowName , threshold1_default, alpha_slider_max, set_threshold1)
cv2.createTrackbar(trackbar2_name, windowName , threshold1_default, alpha_slider_max, set_threshold1)

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_mask_nores.avi')
# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39.mp4')
# o_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_test_res_len1_pan.png')

cap = cv2.VideoCapture(v_name)
ret, img = cap.read()
while ret:
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0) 

    # # Sobel Edge Detection
    # sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    # sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    # sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection

    # # Display Sobel Edge Detection Images
    # cv2.imshow('Sobel X', sobelx)
    # # cv2.waitKey(0)

    # cv2.imshow('Sobel Y', sobely)
    # # cv2.waitKey(0)

    # cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
    edges = cv2.Canny(image=img_blur, threshold1=threshold1_value, threshold2=threshold2_value) 
    
    cv2.imshow(windowName, edges)
    cv2.imshow('Original', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('e'):
        ret, img = cap.read()