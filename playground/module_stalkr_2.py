import numpy as np
import cv2 as cv
import matplotlib
from matplotlib import pyplot as plt
import os
import sys
np.set_printoptions(threshold=sys.maxsize)
# matplotlib.use('linuxfb')


path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/tsukuba_l.png')
path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/tsukuba_r.png')

imgL = cv.imread(path1,0)
imgR = cv.imread(path2,0)

stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)

# print(type(disparity))

# disparity = disparity + 17 
# disparity = np.abs(disparity)
# print(imgL)
# plt.imshow(disparity,'gray')
# plt.show()

# cv.imshow('imgL',imgL)
# cv.imshow('imgR',imgR)

# cv.normalize(disparity, disparity, 0, 255, cv.NORM_MINMAX)
norm_image = cv.normalize(disparity, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
# print(disparity)
print(np.max(norm_image))
cv.imshow('disparity',norm_image)
cv.waitKey(0)
