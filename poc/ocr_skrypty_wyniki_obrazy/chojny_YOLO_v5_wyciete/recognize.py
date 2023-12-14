#######################################################################################################################################################

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import easyocr
import random
import math
import cv2
import sys


#######################################################################################################################################################

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
                return None
            else:
                v = int(v1 / v2)
            xq.append(v)
        d = np.sum(np.abs(vq - xq))
        if (d == 0):
            break
    return [xq, tq, M]


#######################################################################################################################################################

def filterQII(img, A, B):
    L = 2
    (width, height) = img.shape
    N = width * height
    while (True):
        x = np.reshape(np.array(img[:][:]), N)
        # ////////////////////////////////////////////////////////////////////////////////
        v = LoydMax(x, L, N)
        if (v == None):
            return img
        [xq, tq, M] = v
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
    # ////////////////////////////////////////////////////////////////////////////////
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


#######################################################################################################################################################

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


#######################################################################################################################################################

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


#######################################################################################################################################################


def find_numbers_on_image_gen(dir_path: str):
    flist = os.listdir(dir_path)
    ftext = ''

    for f in flist:
        name = dir_path + f
        img = cv2.imread(name)
        # ////////////////////////////////////////////////////////////////////////////////
        # contrast enhancement
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (height, width) = np.shape(img)
        S = 150 / height
        img = cv2.resize(img, (int(S * width), int(S * height)), cv2.INTER_LINEAR)
        img = filterQII(img, 1, 35)
        img2 = img.copy()
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        result = reader.detect(img)[0]
        for rs in result:
            for rb in rs:
                cv2.rectangle(img2, (rb[0], rb[2]), (rb[1], rb[3]), 255, 2)
        result = reader.readtext(img)
        text = ''
        for rr in result:
            text += rr[1]
        rr = check_number(text)

        file_name = f
        read_text = text
        read_number = rr[0]
        number_is_found = rr[1]

        yield file_name, read_text, number_is_found, read_number


if __name__ == '__main__':
    dir_path = './images/'

    for file_name, read_text, number_is_found, read_number in find_numbers_on_image_gen(dir_path):
        if number_is_found:
            print(file_name, ', text = \"', read_text, '\" -> recognized: ', number_is_found, sep='')
        else:
            print(file_name, ', text = \"', read_text, '\" -> not recognized', sep='')
