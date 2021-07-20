import os
import cv2
import numpy as np
from skimage.morphology import closing,disk


# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_1.mp4')
# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_3_3.mp4')
v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39.mp4')
# f_name_full = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_full.png')
# f_name_disp = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_disp.png')

dir_name = v_name[:-4]

try:
    os.mkdir(dir_name)
except:
    pass


cap = cv2.VideoCapture(v_name)
windowNameD = 'cmp'
cv2.namedWindow(windowNameD, cv2.WINDOW_FREERATIO)
cv2.namedWindow('xdd', cv2.WINDOW_FREERATIO)
cv2.resizeWindow(windowNameD, 1280, 720)


ret, imgL = cap.read() 
ret, imgR = cap.read() 
windowSize = (imgR.shape[1], imgR.shape[0])
# resizeSize = (1280, 720)
# resizeSize = (640, 360)


out_name = v_name[:-4] + '_V3_test_resv' + '.avi'
# out_cap = cv2.VideoCapture(0)
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# def just_print_for_all(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print(x, y)
# cv2.setMouseCallback("xdd", just_print_for_all)
keyPoints = (
             (25*3, 275*3),
             (27*3, 107*3),
             (462*3, 119*3),
             (463*3, 240*3)
             )
# keyPoints = (
#              (25, 275),
#              (27, 107),
#              (462, 119),
#              (463, 240)
#              )



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
    
    # disp2 = np.dstack((disp, disp, disp))
    return disp

wagon_counter = 0
while ret:
    # imgL = cv2.resize(imgL, resizeSize)
    # imgR = cv2.resize(imgR, resizeSize)

    dispV3 = getDispV3(imgL, imgR)
    dispV3[dispV3 > 40] = 255
    dispV3[dispV3 <= 40] = 0
    dispV3 = cv2.medianBlur(dispV3,5)
    kernel = np.ones((3,3), np.uint8)
    dispV3 = cv2.erode(dispV3, kernel)
    kernell = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closing = cv2.morphologyEx(dispV3, cv2.MORPH_CLOSE, kernell)
    # cv2.imshow("xdd", dispV3)
    cv2.imshow("xdd", closing)

    

    imgL[dispV3 == 0] = 0


    # check = dispV3[107*3:275*3, 25*3:27*3] # capacity - 507
    # check = dispV3[125:222, 462:463] # capacity - 244
    check = dispV3[125*3:222*3, 462*3:463*3] # capacity - 244
    
    
    val = cv2.countNonZero(check)
    # print(len(val))
    # cv2.imshow("xkurwade", check)
    
    # TODO threshold 240 => printScreen
    # TODO zamiast printScreen - jazda z paskie na prawo wzdłuż wektora, i printScreen aż do drugiego paska
    # val = None
    # if val < 240*3:
    # if val < 240:
    # print(val)
    if val <= 70*3*3 and val > 0:
        img_wagon = imgL[:, :463*3]
        # file_name = print('%s/%s.png' % (dir_name , str(wagon_counter).zfill(3)))
        file_name = '%s/%s_hd.png' % (dir_name , str(wagon_counter).zfill(3))
        cv2.imwrite(file_name, img_wagon)
        # print('Photo #%3d saved' % wagon_counter)
        print(val)
        wagon_counter += 1

    image = cv2.rectangle(imgL, (463*3, 119*3), (462*3, 240*3), (255, int(val/2), int(val/2)), 1)
    image = cv2.rectangle(imgL, (27*3, 107*3), (25*3, 275*3), (255, int(val/2), int(val/2)), 1)
    # image = cv2.rectangle(imgL, (449, 125), (450, 222), (255, int(val/2), int(val/2)), 1)
    # image = cv2.rectangle(imgL, (27, 107), (25, 275), (255, int(val/2), int(val/2)), 1)
    cv2.imshow(windowNameD, imgL)

    imgL = imgR
    # imgTemp = imgR
    ret, imgR = cap.read()
    frames_left -= 1
    if frames_left % 10 == 0:
        print(frames_left, " frames left")
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('e'):
        ret, img = cap.read()
    
    # k = cv2.waitKey() & 0xFF
    # if k == ord('q'):
    #     break
    # elif k == ord('s'):
    #     cv2.imwrite(f_name_full, imgL)
    #     cv2.imwrite(f_name_disp, dispV3)
    
# out_out.release()
cap.release()
cv2.destroyAllWindows()