import numpy as np
import cv2 as cv
from skimage import restoration, color, util

class Deblur:
    def __init__(self, kernel_len=51):
        self.kernel_len = kernel_len
        self.coef = 0
        self.psf = None
        # self.set_speed(x,y,blur)


    def set_speed(self, x, y, blur, coef):
        self.coef = coef
        precision = 5
        img = np.zeros((self.kernel_len*precision, self.kernel_len*precision), np.float32)
        point = (self.kernel_len*precision // 2, self.kernel_len*precision // 2)
        
        # cv.ellipse(img, point, (0, round(len / 2)), 90 - theta, 0, 360, 255, -1)
        cv.line(img, (point[0]-x//2, point[1]-y//2 ), (point[0]+x//2, point[1]+y//2), 255, 1)

        img = cv.GaussianBlur(img,(0,0),blur, blur)

        img = cv.resize(img, (self.kernel_len, self.kernel_len), interpolation=cv.INTER_AREA)
        summa = np.sum(img)


        # self.psf = cv.cvtColor(img / summa, cv.COLOR_GRAY2RGB) 
        # self.psf = color.gray2rgb(img / summa)
        self.psf = img / summa 

        return self.psf  

    def restore(self, frame):
        result = restoration.wiener(frame, self.psf, self.coef)
        # result = restoration.unsupervised_wiener(frame, self.psf)
        # result = restoration.richardson_lucy(frame, self.psf, num_iter=1)   
        # 
        return result         

    def next(self, frame):
        frame = util.img_as_float64(frame)
        b,g,r = cv.split(frame)
        b = self.restore(b)
        g = self.restore(g)
        r = self.restore(r)
        result = cv.merge([r, g, b])
        result = util.img_as_ubyte(result)

   

        print(np.array2string(self.psf[self.kernel_len//2,:], precision=2)) 

        return result 