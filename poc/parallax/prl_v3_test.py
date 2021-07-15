import os
import cv2
import numpy as np

# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')
v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39.mp4')
f_name_full = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_full.png')
f_name_disp = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_disp.png')

cap = cv2.VideoCapture(v_name)
windowNameD = 'cmp'
cv2.namedWindow(windowNameD, cv2.WINDOW_FREERATIO)
cv2.resizeWindow(windowNameD, 1280, 720)


ret, imgR = cap.read() 
windowSize = windowSize = (imgR.shape[1], imgR.shape[0])
# resizeSize = (1280, 720)
resizeSize = (640, 360)
imgL = imgR
ret, imgR = cap.read() 

out_name = v_name[:-4] + '_V3_test_resv_lam' + '.avi'
# out_cap = cv2.VideoCapture(0)
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0] * 2, windowSize[1] * 2))
out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (resizeSize[0] * 2, resizeSize[1]))

frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)


wsizeV3 = 7
max_dispV3 = 160
wls_lambdaV3 = 8000
wls_sigmaV3 = 1.5

left_matcherV3 = cv2.StereoSGBM_create()
wls_filterV3 = cv2.ximgproc.createDisparityWLSFilter(left_matcherV3)
right_matcherV3 = cv2.ximgproc.createRightMatcher(left_matcherV3)

def getDispV3(imgL, imgR):
    left_for_matcher = cv2.cvtColor(imgL,  cv2.COLOR_BGR2GRAY)
    right_for_matcher = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    left_disp = left_matcherV3.compute(left_for_matcher, right_for_matcher)
    right_disp = right_matcherV3.compute(right_for_matcher, left_for_matcher)

    wls_filterV3.setLambda(wls_lambdaV3)
    wls_filterV3.setSigmaColor(wls_sigmaV3)
    filtered_disp = wls_filterV3.filter(left_disp,imgL,disparity_map_right=right_disp)

    vis = cv2.ximgproc.getDisparityVis(filtered_disp)
    disp = cv2.normalize(vis, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    
    disp2 = np.dstack((disp, disp, disp))
    return disp2


def getDispClear(disp):
    disp4 = np.copy(disp)
    np.putmask(disp4, disp4 < disp4.max(), 0)
    return disp4

def concImages(imgL, dispV3):
    ###########################
    #            #            #
    #    imgL    #   dispV3   #
    #            #            #
    ###########################

    both = np.concatenate((imgL, dispV3), axis = 1)
    return both

while ret:
    imgL = cv2.resize(imgL, resizeSize)
    imgR = cv2.resize(imgR, resizeSize)

    dispV3 = getDispV3(imgL, imgR)
    conc = concImages(imgL, dispV3)
    cv2.imshow(windowNameD, conc)

    out_out.write(conc)
    imgL = imgR
    ret, imgR = cap.read()
    frames_left -= 1
    if frames_left % 10 == 0:
        print(frames_left, " frames left")
    k = cv2.waitKey() & 0xFF
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite(f_name_full, imgL)
        cv2.imwrite(f_name_disp, dispV3)
    
out_out.release()
cap.release()
cv2.destroyAllWindows()