import cv2
import numpy as np
import os
import skimage
import skimage.color as skc
import skimage.segmentation as sks


def getDispClear(disp):
    disp4 = np.copy(disp)
    np.putmask(disp4, disp4 > 0, 255)
    return disp4

f_name_full = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_full.png')
f_name_disp = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_disp.png')
f_name_rw   = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_rw.png')

# Load photo
image_full = cv2.imread(f_name_full)
image_disp = cv2.imread(f_name_disp,0)
# Get one channel
    # done by imread(:,0)
# (maybye) binarise
image_full_gray = cv2.cvtColor(image_full, cv2.COLOR_BGR2GRAY)
image_disp_clear = getDispClear(image_disp)

# Erode a little
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(image_disp_clear,kernel,iterations = 1)
cv2.imshow("erosion", erosion)
cv2.waitKey(0)
# Get what's left as "markers"
image_marker = skimage.img_as_ubyte(skc.rgb2gray(erosion))
# Random Wanker

image_final = sks.random_walker(image_full_gray, image_marker, beta = 10, mode = "bf")

cv2.imwrite(f_name_rw, image_final)

cv2.imshow("image_final", image_final)
cv2.waitKey(0)