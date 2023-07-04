import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from scipy.signal import convolve2d as conv2

from skimage import color, io, restoration

show_window = "deconv"
ctrl_window = "ctrl"

img = color.rgb2gray(io.imread('23_24_1698.png'))
# img = img[355:470, 1301:1450]

kernel_len = 51

zoom = 1
show_zoom = 1

img = cv.resize(img, np.array(np.shape(img))*zoom)



def calcPSF(len, theta, blur):
    precision = 5
    img = np.zeros((kernel_len*precision, kernel_len*precision), np.float32)
    point = (kernel_len*precision // 2, kernel_len*precision // 2)
    
    cv.ellipse(img, point, (0, round(len / 2)), 90 - theta, 0, 360, 255, -1)

    img = cv.GaussianBlur(img,(0,0),blur, blur)

    img = cv.resize(img, (kernel_len, kernel_len), interpolation=cv.INTER_AREA)
    summa = np.sum(img)
    return img / summa


def recalc(tmp):
    # len = 11 * zoom * cv.getTrackbarPos('length', ctrl_window) / 100
    len = zoom * cv.getTrackbarPos('length', ctrl_window)
    theta = cv.getTrackbarPos('theta', ctrl_window)
    blur = cv.getTrackbarPos('blur', ctrl_window) / 5
    magic = cv.getTrackbarPos('magic', ctrl_window) 

    psf = calcPSF(len, theta, blur)

    img_deconv = restoration.wiener(img, psf, magic / 1000)
    # img_deconv = restoration.unsupervised_wiener(img, psf)
    # img_deconv = restoration.richardson_lucy(img, psf, num_iter=magic+1)

    cv.imshow(show_window, cv.resize(img_deconv, np.array(np.shape(img_deconv))*show_zoom))
    cv.imshow("psf", cv.resize(psf, np.array(np.shape(psf))*show_zoom))

    print(np.array2string(psf[kernel_len//2,:], precision=2)) 


cv.imshow(show_window, cv.resize(img, np.array(np.shape(img))*show_zoom))

cv.namedWindow(ctrl_window,cv.WINDOW_NORMAL)
cv.createTrackbar(f"length", ctrl_window, 0, 200, recalc)
cv.createTrackbar(f"theta", ctrl_window, 0, 180, recalc)
cv.createTrackbar(f"blur", ctrl_window, 1, 100, recalc)
cv.createTrackbar(f"magic", ctrl_window, 1, 2000, recalc)

recalc(123)
cv.waitKey()