



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
    return disp

wsizeV3 = 7
max_dispV3 = 160
wls_lambdaV3 = 8000
wls_sigmaV3 = 1.5

left_matcherV3 = cv2.StereoSGBM_create()
wls_filterV3 = cv2.ximgproc.createDisparityWLSFilter(left_matcherV3)
right_matcherV3 = cv2.ximgproc.createRightMatcher(left_matcherV3)


dispV3 = getDispV3(imgL, imgR)