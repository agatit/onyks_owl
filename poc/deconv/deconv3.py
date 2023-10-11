import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from scipy.signal import convolve2d as conv2

from skimage import color, io, restoration, util

from deblur import Deblur

show_window = "deconv"
ctrl_window = "ctrl"

img = io.imread('poc/23_24_1698.png')
# img = color.rgb2gray(img)

# img = img[355:470, 1301:1450]

zoom = 1
show_zoom = 1
img = cv.resize(img, np.array(img.shape[0:2])*zoom)

deblur = Deblur(51)

def recalc(tmp):
    # len = 11 * zoom * cv.getTrackbarPos('length', ctrl_window) / 100
    x = cv.getTrackbarPos('x', ctrl_window)
    y = cv.getTrackbarPos('y', ctrl_window)
    blur = cv.getTrackbarPos('blur', ctrl_window) / 5
    coef = cv.getTrackbarPos('magic', ctrl_window) / 1000

    psf = deblur.set_speed(x, y, blur, coef)
    img_deconv = deblur.get_raw_velocity(img)


    cv.imshow(show_window, cv.resize(img_deconv, np.array(img_deconv.shape[0:2])*show_zoom))
    cv.imshow("psf", cv.resize(psf, np.array(np.shape(psf))*show_zoom))    


cv.imshow(show_window, cv.resize(img, np.array(img.shape[0:2])*show_zoom))

cv.namedWindow(ctrl_window,cv.WINDOW_NORMAL)
cv.createTrackbar(f"x", ctrl_window, 0, 200, recalc)
cv.createTrackbar(f"y", ctrl_window, 0, 200, recalc)
cv.createTrackbar(f"blur", ctrl_window, 1, 100, recalc)
cv.createTrackbar(f"magic", ctrl_window, 1, 2000, recalc)

recalc(123)
cv.waitKey()