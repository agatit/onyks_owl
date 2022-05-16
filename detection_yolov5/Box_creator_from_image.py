"""
Program do tworzenia zbiorów do nauki w formacie yolov5 z zdjęć rzeczywistych bez masek. 

Do poprawnego działania potrzebna możliwość wyświetlania zdjęć i folder z zdjęciami.


Efektem pracy programu jest:
  -przeniesienie wykorzystanego zdjęcia do folderu "used"
  -folder "results" z dwoma podfolderami "images", "labels" w których kolejno znajdują się zdjęcia i opisy w formacie yolo (label, center_x, center_y, with, height)
   przy czym infromacje te są zapisywane w postaci
   (wartość / maksymalna_wartość_dla_zdjecia np. center_x = położenie_srodka_obiektu_w_osi_x_w_pixelach / cała_szerokość_obrazu).
   

Położenie oryginału: 
"""


import cv2 as cv
import numpy as np
import sys
import os 

folder = "C:\\Users\\Marcin\\Agat_IT\\Yolo_v5\\Images_without_boxes"    #scieżka do folderu z którego ma pobrać zdjęcia 
label_dict =   ["vertical_text",                                        #lista labeli przypisanych do kolejnych numerów na klawiaturze
                "horizontal_text",
                "container_corner",
                "label_4", 
                "railcar_bogie",
                "railcar_text",
                "label_7",
                "label_8",
                "label_9",
                "label_0"]

TVT_ratio = [70,20,10]                                                  #stosunek podziału odpowiednich zdjęć      

dirName = os.path.join(folder, "results")
    
# Create target directory & all intermediate directories if don't exists
try:
    os.makedirs(dirName)    
    print("Directory " , dirName ,  " Created ")
    
except FileExistsError:
    print("Directory " , dirName ,  " already exists")  

dirName = os.path.join(folder, "used")
    
# Create target directory & all intermediate directories if don't exists
try:
    os.makedirs(dirName)    
    print("Directory " , dirName ,  " Created ")
    
except FileExistsError:
    print("Directory " , dirName ,  " already exists") 

dirName = os.path.join(folder, "results","images")
    
# Create target directory & all intermediate directories if don't exists
try:
    os.makedirs(dirName)    
    print("Directory " , dirName ,  " Created ")
    
except FileExistsError:
    print("Directory " , dirName ,  " already exists")  

dirName = os.path.join(folder, "results", "labels")
    
# Create target directory & all intermediate directories if don't exists
try:
    os.makedirs(dirName)    
    print("Directory " , dirName ,  " Created ")
    
except FileExistsError:
    print("Directory " , dirName ,  " already exists")  

a = 0 
def none(a):
    pass


for file in os.listdir(folder):
    img = cv.imread(os.path.join(folder, file))
    label = []
    center_x = []
    center_y = []
    width = []
    height = []

    w_0, h_0, ch_0 = img.shape
    if a ==0:
        cv.namedWindow("ROI")
        cv.createTrackbar("vertical_left", "ROI", 0, h_0, none)
        cv.createTrackbar("vertical_right", "ROI", h_0, h_0, none)
        cv.createTrackbar("horizontal_up", "ROI", 0, w_0, none)
        cv.createTrackbar("horizontal_down", "ROI", w_0, w_0, none)
        a = 1
    elif a==1:
        cv.setTrackbarMax("vertical_left", "ROI", h_0)
        cv.setTrackbarMax("vertical_right", "ROI", h_0)
        cv.setTrackbarMax("horizontal_up", "ROI", w_0)
        cv.setTrackbarMax("horizontal_down", "ROI", w_0)
        cv.setTrackbarPos("vertical_left", "ROI", 0)
        cv.setTrackbarPos("vertical_right", "ROI", h_0)
        cv.setTrackbarPos("horizontal_up", "ROI", 0)
        cv.setTrackbarPos("horizontal_down", "ROI", w_0)
    while(1):
        frame = img.copy()
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(255,0,0), 3) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 3) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 3) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 3) 

        cv.imshow("img", frame)
        k = cv.waitKey(1)
        if k == ord("1"):
            label.append(0)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("2"):
            label.append(1)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("3"):
            label.append(2)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("4"):
            label.append(3)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("5"):
            label.append(4)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("6"):
            label.append(5)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("7"):
            label.append(6)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("8"):
            label.append(7)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("9"):
            label.append(8)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("0"):
            label.append(9)
            x1 = cv.getTrackbarPos("vertical_left", "ROI")
            y1 = cv.getTrackbarPos("horizontal_up", "ROI")
            x2 = cv.getTrackbarPos("vertical_right", "ROI")
            y2 = cv.getTrackbarPos("horizontal_down", "ROI")

            center_x.append(((x2 + x1)/2)/h_0)
            center_y.append(((y2 + y1)/2)/w_0)
            width.append((x2-x1)/h_0)
            height.append((y2 - y1)/w_0)
        if k == ord("q"):
            break
    
    cv.imwrite(os.path.join(folder, "results", "images", file), img)
    cv.imwrite(os.path.join(folder, "used", file), img)
    os.remove(os.path.join(folder, file))
    file = open(os.path.join(folder, "results", "labels",str(file[:-4]+".txt")), 'w')
    for num, element in enumerate(label):
        x = num -1
        file.write(f"{label[x]} {center_x[x]} {center_y[x]} {width[x]} {height[x]}\n")
    file.close()
    file = open(os.path.join(folder, "results","data.yaml"), 'w')
    file.write("names:\n")
    for element in label_dict:
        file.write(f"- {element}\n")
    file.write(f"nc: {len(label_dict)}\ntrain: \nval: ")


    file.close()
    

    
