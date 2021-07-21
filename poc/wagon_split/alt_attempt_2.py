import os
import cv2
import numpy as np
from skimage.morphology import closing,disk




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

cap = cv2.VideoCapture(v_name)
windowNameD = 'cmp'
cv2.namedWindow(windowNameD, cv2.WINDOW_FREERATIO)
cv2.resizeWindow(windowNameD, 1280, 720)


ret, imgL = cap.read() 

windowSize = windowSize = (imgL.shape[1], imgL.shape[0])
# resizeSize = (1280, 720)
# resizeSize = (640, 360)


# out_name = v_name[:-4] + '_V3_mask_nores_edges' + '.avi'
# out_cap = cv2.VideoCapture(0)
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0] * 2, windowSize[1] * 2))
# out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0], windowSize[1]))

frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)

ret, imgL = cap.read()
while ret:

    img_blur = cv2.medianBlur(imgL,5)
    edges = cv2.Canny(image=img_blur, threshold1=threshold1_value, threshold2=threshold2_value) 

    # kernel = np.ones((3,3), np.uint8)
    # dispV3 = cv2.erode(dispV3, kernel)
    cv2.imshow(windowNameD, imgL)
    cv2.imshow(windowName, edges)
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('e'):
        ret, imgL = cap.read()
        frames_left -= 1
        if frames_left % 10 == 0:
            print(frames_left, " frames left")
    
cap.release()
cv2.destroyAllWindows()