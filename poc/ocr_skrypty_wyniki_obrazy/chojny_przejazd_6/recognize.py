import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # for easy ocr DLLs
import matplotlib.pyplot as plt
import numpy as np
import easyocr
import math
import cv2
import sys


##########################################################################################

def adjustGamma(img, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)


##########################################################################################

def brightnessContrast(img, brightness=255, contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
        al_pha = (max - shadow) / 255
        ga_mma = shadow
        cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma)
    else:
        cal = img
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)
    return cal


##########################################################################################

def equalizeImg(img, n):
    clahe = cv2.createCLAHE(clipLimit=n)
    img[:, :, 0] = clahe.apply(img[:, :, 0])
    img[:, :, 1] = clahe.apply(img[:, :, 1])
    img[:, :, 2] = clahe.apply(img[:, :, 2])
    return img


##########################################################################################

def perspective_correction(img, M1, M2):
    global pp
    matrix = cv2.getPerspectiveTransform(M1, M2)
    img = cv2.warpPerspective(img, matrix, (1504, 320))
    return img


##########################################################################################

def LoydMax(x, L, N):
    m1 = np.min(x)
    m2 = np.max(x)
    M = int(m2 - m1 + 1)
    H = np.zeros(M, float)
    for i in range(0, N):
        v = int(x[i] - m1)
        H[v] += 1
    E = 1000
    xq = list()
    tq = list()
    # xq values
    for i in range(0, L):
        x = int(i * M / L) + int(0.5 * M / L)
        xq.append(x)
    for e in range(0, E):
        # tq values
        tq = list()
        tq.append(0.0)
        for i in range(0, L - 1):
            t = int(np.ceil((xq[i] + xq[i + 1]) / 2.0))
            tq.append(t)
        tq.append(M - 1)
        # new xq
        vq = np.copy(xq)
        xq = list()
        for i in range(0, L):
            v1 = 0
            v2 = 0
            for j in range(int(tq[i]), int(tq[i + 1])):
                v1 = v1 + H[j] * j
                v2 = v2 + H[j]
            if (v2 == 0):
                print('QII critical error.')
                quit()
            else:
                v = int(v1 / v2)
            xq.append(v)
        d = np.sum(np.abs(vq - xq))
        if (d == 0):
            break
    return [xq, tq, M]


##########################################################################################

def filterQII(img, A, B):
    L = 2
    (width, height) = img.shape
    N = width * height
    while (True):
        x = np.reshape(np.array(img[:][:]), N)
        # //////////////////////////////////////
        [xq, tq, M] = LoydMax(x, L, N)
        Q = np.zeros(M, int)
        for i in range(0, L):
            m1 = int(tq[i])
            m2 = int(tq[i + 1])
            mm = int(xq[i])
            for j in range(m1, m2 + 1):
                Q[j] = mm
        n1 = np.min(x)
        er = 0
        for i in range(0, N):
            w = x[i] - n1
            v = Q[w]
            er = er + (v - w) ** 2
        er /= N
        psnr = 10.0 * math.log(255 ** 2 / er) / math.log(10)
        if (psnr > B):
            break
        L = L + 1
    # //////////////////////////////////////
    n1 = np.min(x)
    m1 = 0
    m2 = tq[L - 1]
    LUT = np.zeros(256, float)
    for i in range(0, m2):
        LUT[i] = 0
    for i in range(m2, 256):
        LUT[i] = 255
    for i in range(m1, m2):
        LUT[i] = 255 * (math.exp(A * (i - m1) / (m2 - m1)) - 1) / (math.exp(A) - 1)
    for i in range(0, width):
        for j in range(0, height):
            img[i][j] = LUT[img[i][j] - n1]
    return img


##########################################################################################

def calc_sum(str):
    s = 0
    for i in range(0, 11):
        if (i % 2 == 0):
            v = 2 * int(str[i])
            if (v >= 10):
                s = s + v // 10
                s = s + v % 10
            else:
                s = s + v
        else:
            s = s + int(str[i])
    s = 10 * math.ceil(s / 10) - s
    return s


##########################################################################################

ccodes = ['51', '80', '31', '54']  # country codes


def check_number(text):
    fr = ['', False]
    t = ''
    for i in range(0, len(text)):
        if (text[i] >= '0' and text[i] <= '9'):
            t = t + text[i]
    text = t
    if (text != ''):
        if (len(text) >= 12):
            for i in range(0, len(text) - 11):
                t = text[i:i + 12]
                s = calc_sum(t)
                if (s == int(t[11]) and (t[2:4] in ccodes)):
                    fr[0] = text[i:i + 12]
                    fr[1] = True
                    break
    return fr


##########################################################################################

if __name__ == '__main__':

    fpath = './images/'
    flist = os.listdir(fpath)
    ftext = ''
    fshow = False

    for f in flist:
        name = fpath + f
        print(120 * '-')
        print('File:', f)
        # //////////////////////////////////////
        # Load image
        img = cv2.imread(name)
        # //////////////////////////////////////
        # Perspective correction
        M1 = np.float32([[160, 340], [1800, 500], [120, 680], [1800, 760]])
        M2 = np.float32([[0, 0], [1632, 0], [0, 320], [1632, 320]])
        img = perspective_correction(img, M1, M2)
        img = img[16:-16, 160:-160]
        # contrast enhancement
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = filterQII(img, 5, 30)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        # //////////////////////////////////////
        # Detect text
        model = cv2.dnn.readNet('frozen_east_text_detection.pb')
        # find text areas
        height, width, colorch = img.shape
        img = img.copy()
        blob = cv2.dnn.blobFromImage(img, 1, (width, height), (124, 117, 104), True, False)
        model.setInput(blob)
        (geometry, scores) = model.forward(model.getUnconnectedOutLayersNames())
        rectangles = []
        confidence_score = []
        for i in range(geometry.shape[2]):
            for j in range(0, geometry.shape[3]):
                if scores[0][0][i][j] < 0.1:
                    continue
                bottom_x = int(j * 4 + geometry[0][1][i][j])
                bottom_y = int(i * 4 + geometry[0][2][i][j])
                top_x = int(j * 4 - geometry[0][3][i][j])
                top_y = int(i * 4 - geometry[0][0][i][j])
                rectangles.append([top_x, top_y, bottom_x, bottom_y])
                confidence_score.append(float(scores[0][0][i][j]))
        # //////////////////////////////////////
        # create buffer/draw rectangles
        img2 = np.zeros((height, width), np.uint8)
        for [x1, y1, x2, y2] in rectangles:
            img2 = cv2.rectangle(img2, (x1, y1), (x2, y2), 255, 8)
        # //////////////////////////////////////
        # dilate/find contour/draw contours
        bounding_rects = list()
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
        img2 = cv2.dilate(img2, dilate_kernel, iterations=3)
        cnts, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            x, y, w, h = cv2.boundingRect(cv2.approxPolyDP(c, 3, True))
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            bounding_rects.append([x, y, w, h, '', 0])
        # //////////////////////////////////////
        # Text recognition
        S = 4  # scale factor
        img_list = list()
        for i in range(0, len(bounding_rects)):
            r = bounding_rects[i]
            img2 = cv2.resize(img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]], (S * r[2], S * r[3]))
            # preprocessing
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            # connecting elements
            mask = np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]],
                            np.uint8)
            img2 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, mask)
            # recognize
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            result = reader.readtext(img2)
            text = ''
            tlc = 0
            num = 0
            for rr in result:
                text += rr[1]
                tlc += rr[2]
                num += 1
            if (num > 0):
                tlc /= num
            bounding_rects[i][4] = text
            bounding_rects[i][5] = tlc
            # //////////////////////////////////////
            tt = check_number(text)
            print('Rect = (x:%d,y:%d,w:%d,h:%d),' % (r[0], r[1], r[2], r[3]), end=' ')
            if (tt[1] == True):
                print('Recognition = True, Text = \"', text, '\"', ' -> ', tt[0], sep='')
            else:
                print('Recognition = False, Text = \"', text, '\"', sep='')
            # //////////////////////////////////////
            if (fshow == True):
                plt.imshow(img2, cmap='gray')
                plt.show()
