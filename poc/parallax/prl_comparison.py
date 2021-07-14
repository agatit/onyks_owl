import os
import cv2
import numpy as np

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')

cap = cv2.VideoCapture(v_name)
windowNameD = 'cmp'
cv2.namedWindow(windowNameD, cv2.WINDOW_FREERATIO)
cv2.resizeWindow(windowNameD, 1280, 720)

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
windowSize = windowSize = (imgR.shape[1], imgR.shape[0])
imgL = imgR
ret, imgR = cap.read() 

out_name = v_name[:-4] + '_prl_cmp' + '.avi'
# out_cap = cv2.VideoCapture(0)
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0] * 2, windowSize[1] * 2))

frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)


wsize = 7
max_disp = 160
wls_lambda = 8000
wls_sigma = 1.5

left_matcher = cv2.StereoBM_create()
wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher)
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

def getDispV1(imgL, imgR):
    disp = stereo.compute(imgL, imgR).astype(np.float32)
    disp = cv2.normalize(disp, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U) 
    disp2 = np.dstack((disp, disp, disp))
    return disp2

def getDispV2(imgL, imgR):
    left_for_matcher = cv2.cvtColor(imgL,  cv2.COLOR_BGR2GRAY)
    right_for_matcher = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    left_disp = left_matcher.compute(left_for_matcher, right_for_matcher)
    right_disp = right_matcher.compute(right_for_matcher, left_for_matcher)

    wls_filter.setLambda(wls_lambda)
    wls_filter.setSigmaColor(wls_sigma)
    filtered_disp = wls_filter.filter(left_disp,imgL,disparity_map_right=right_disp)

    vis = cv2.ximgproc.getDisparityVis(filtered_disp)
    disp = cv2.normalize(vis, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    
    disp2 = np.dstack((disp, disp, disp))
    return disp2

def getDispClear(disp):
    disp4 = np.copy(disp)
    np.putmask(disp4, disp4 < disp4.max(), 0)
    return disp4

def concImages(imgL, imgR, dispV1, dispV2):
    ###########################
    #            #            #
    #    imgL    #    imgR    #
    #            #            #
    ###########################
    #            #            #
    #   dispV1   #   dispV2   #
    #            #            #
    ###########################
    up = np.concatenate((imgL, imgR), axis = 1)
    down = np.concatenate((dispV1, dispV2), axis = 1)
    both = np.concatenate((up, down), axis = 0)
    return both

while ret:
    imgL = cv2.resize(imgL, windowSize)
    imgR = cv2.resize(imgR, windowSize)

    dispV1 = getDispV1(imgL, imgR)
    dispV2 = getDispV2(imgL, imgR)
    conc = concImages(imgL, imgR, dispV1, dispV2)

    cv2.imshow(windowNameD, conc)

    out_out.write(conc)
    imgL = imgR
    ret, imgR = cap.read()
    frames_left -= 1
    if frames_left % 10 == 0:
        print(frames_left, " frames left")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
out_out.release()
cap.release()
cv2.destroyAllWindows()