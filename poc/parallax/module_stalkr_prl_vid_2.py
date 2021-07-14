import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

cv2.namedWindow("vis", cv2.WINDOW_FREERATIO)
cv2.resizeWindow("vis", 1280, 720)

def concImages(imgL, imgR, dispNorm):
    ###########################
    #            #            #
    #    imgL    #    imgR    #
    #            #            #
    ###########################
    #            #            #
    #  dispNorm  # dispClear  #
    #            #            #
    ###########################
    # PREVIOUS VERSION WITH 3 IMAGES
    windowSize = (imgL.shape[1], imgL.shape[0])
    preconc = np.concatenate((imgL, imgR), axis = 1)
    conc = np.concatenate((preconc, np.zeros_like(preconc)), axis = 0)
    conc[windowSize[1]:,int(windowSize[0]/2):int(windowSize[0]/2+windowSize[0])] = dispNorm
    """
    up = np.concatenate((imgL, imgR), axis = 1)
    down = np.concatenate((dispNorm, dispClear), axis = 1)
    both = np.concatenate((up, down), axis = 0)
    """
    return conc

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')
cap = cv2.VideoCapture(v_name)
ret, imgR = cap.read() 

imgL = imgR
ret, imgR = cap.read() 

# no downscale :)
# left_for_matcher = left
# right_for_matcher = right

wsize = 7
max_disp = 160
wls_lambda = 8000
wls_sigma = 1.5

# wersja z StereoBM
left_matcher = cv2.StereoBM_create()
wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher)
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

out_name = v_name[:-4] + 'out' + '.avi'
# out_cap = cv2.VideoCapture(0)
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (1920 * 2, 1080 * 2))

while True:
    left_for_matcher = cv2.cvtColor(imgL,  cv2.COLOR_BGR2GRAY)
    right_for_matcher = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    left_disp = left_matcher.compute(left_for_matcher, right_for_matcher)
    right_disp = right_matcher.compute(right_for_matcher, left_for_matcher)

    wls_filter.setLambda(wls_lambda)
    wls_filter.setSigmaColor(wls_sigma)
    filtered_disp = wls_filter.filter(left_disp,imgL,disparity_map_right=right_disp)

    vis = cv2.ximgproc.getDisparityVis(filtered_disp)
    vis = np.dstack((vis, vis, vis))
    conc = concImages(imgL, imgR, vis)
    out_out.write(conc)
    cv2.imshow("vis",conc)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    imgL = imgR
    ret, imgR = cap.read() 

# cv2.waitKey(0)
out_out.release()
cap.release()
cv2.destroyAllWindows()