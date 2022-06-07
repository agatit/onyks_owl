from distutils import text_file
from linecache import getline
from tkinter.tix import Tree
import cv2 as cv
import os
import numpy as np 

folder = "C:\\Users\\Marcin\\Agat_IT\\Yolo_v5\\Images_without_boxes\\results\\test"

label_dict =   ["vertical_text",
                "horizontal_text",
                "container_corner",
                "label_4", 
                "railcar_bogie",
                "railcar_text",
                "label_7",
                "label_8",
                "label_9",
                "label_0"]

labels_blank = np.ones((500,200,3))
a = 0 
def none(mark):
    pass    

activator = True
quit = False
adding = False
modyfing = False
labeling = False

def label_show( img, list):
    img_copy = img.copy()
    cv.putText(img_copy,"new label", (5,20), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
    x = 5
    y = 50
    for element in list:
        element = element.strip()
        kwant = element.split(" ")
        if kwant[0] != '':
            label_name = label_dict[int(kwant[0])]
            cv.putText(img_copy,label_name, (x,y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
        y +=30
    return(img_copy)

def label_mark(img):        #wyświtlanie znacznika aktywnego labela
    img_copy = img.copy()
    x = 0
    y = mark*30 + 30
    if mark != -1:
        cv.rectangle(img_copy,(x,y),(x+200,y+30),(0,255,255),-1)
        if modyfing == True:
            cv.circle(img_copy, (190,y+15), 3, (0,0,255), -1)
        if labeling == True:
            cv.circle(img_copy, (180,y+15), 3, (255,0,0), -1)
    else:
        cv.rectangle(img_copy,(0,0),(200,30),(0,255,0),-1)



    return(img_copy)

def bars_adjustment(list, mark, img):
    h_i, w_i, ch_i = img.shape
    if mark != -1:
        x_center_yf = []
        y_center_yf = []
        width_yf =    []
        height_yf =   []
        element = list[mark].strip()
        kwant = element.split(" ")
        if kwant[0] != '':
            x_center_yf = float(kwant[1])
            y_center_yf = float(kwant[2])
            width_yf =    float(kwant[3])
            height_yf =   float(kwant[4])

            x_center = x_center_yf * w_i
            y_center = y_center_yf * h_i
            width = width_yf * w_i
            height = height_yf * h_i

            x_1 = int(x_center - (width/2))
            x_2 = int(x_center + (width/2))
            y_1 = int(y_center - (height/2))
            y_2 = int(y_center + (height/2))

            cv.setTrackbarPos("vertical_left", "ROI", x_1)
            cv.setTrackbarPos("vertical_right", "ROI", x_2)
            cv.setTrackbarPos("horizontal_up", "ROI", y_1)
            cv.setTrackbarPos("horizontal_down", "ROI", y_2)
    
    else:
        cv.setTrackbarPos("vertical_left", "ROI", 0)
        cv.setTrackbarPos("vertical_right", "ROI", w_0)
        cv.setTrackbarPos("horizontal_up", "ROI", 0)
        cv.setTrackbarPos("horizontal_down", "ROI", h_0)     
    
def show_image(img):
    img_copy = img.copy()
    sth_changed = False
    w_i, h_i, ch_i = img_copy.shape
    while w_i > 1800 or h_i > 900:
        w_i = w_i * 0.9
        h_i = h_i * 0.9
        sth_changed = True

    while w_i < 500:
        w_i = w_i * 1.1
        h_i = h_i * 1.1
        sth_changed = True
    if sth_changed == True:
        img_copy = cv.resize(img_copy,(int(h_i), int(w_i)), interpolation= cv.INTER_AREA )
    return(img_copy)

def adding_annotation(key):
    
    x1 = cv.getTrackbarPos("vertical_left", "ROI")
    y1 = cv.getTrackbarPos("horizontal_up", "ROI")
    x2 = cv.getTrackbarPos("vertical_right", "ROI")
    y2 = cv.getTrackbarPos("horizontal_down", "ROI")

    center_x = ((x2 + x1)/2)/h_0
    center_y = ((y2 + y1)/2)/w_0
    width = (x2-x1)/h_0
    height = (y2 - y1)/w_0 

    new_annotation = str(key) + ' ' + str(center_x) + ' ' + str(center_y) + ' ' + str(width) + ' ' + str(height)
    object_list.append(new_annotation)


    return()

def modyfing_annotation(mark, list):
    updating_object = list[mark]
    updating_elements = updating_object.split(' ')
    label = updating_elements[0] 
    x1 = cv.getTrackbarPos("vertical_left", "ROI")
    y1 = cv.getTrackbarPos("horizontal_up", "ROI")
    x2 = cv.getTrackbarPos("vertical_right", "ROI")
    y2 = cv.getTrackbarPos("horizontal_down", "ROI")

    center_x = ((x2 + x1)/2)/h_0
    center_y = ((y2 + y1)/2)/w_0
    width = (x2-x1)/h_0
    height = (y2 - y1)/w_0



    new_annotation = str(label) + ' ' + str(center_x) + ' ' + str(center_y) + ' ' + str(width) + ' ' + str(height)
    return(new_annotation)

def save_txt(txt, list):
    full_annotation = ''
    for object in list:
        full_annotation = full_annotation + object + '\n'
    full_annotation = full_annotation[:-2]

    file = open(txt, "w")
    file.write(full_annotation)
    file.close

def change_label(mark, key, list):
    updating_object = list[mark]
    updating_elements = updating_object.split(' ')
    

    new_annotation = str(key) + ' ' + str(updating_elements[1]) + ' ' + str(updating_elements[2]) + ' ' + str(updating_elements[3]) + ' ' + str(updating_elements[4])
    
    list[mark] = new_annotation
    


###### Zczytywanie każdego kolejnego zdjęcia i odpowiadającego mu labela
for file in os.listdir(os.path.join(folder,"img")):
    object_list = []
    mark = 0
    img = cv.imread(os.path.join(folder,"img",file))
    txt_file =  open(os.path.join(folder,"label",str(file[:-4]+".txt")), "r+").read()
    object_list = txt_file.split('\n')
    for object in object_list:
        if object == '':
            object_list.remove('')
    w_0, h_0, ch_0 = img.shape
    if a ==0:
        cv.namedWindow("ROI")
        cv.moveWindow("ROI", 0,800)
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
        if activator == True:
            label_frame = label_mark(labels_blank)
            label_frame = label_show(label_frame,object_list)
            bars_adjustment(object_list, mark, frame)
            activator = False

        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(255,0,0), 1) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 1) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_left", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 1) 
        frame = cv.line(frame,(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_up", "ROI")),(cv.getTrackbarPos("vertical_right", "ROI"),cv.getTrackbarPos("horizontal_down", "ROI")),(255,0,0), 1) 
        cv.imshow("okno pogladowe", show_image(frame) )
        cv.imshow("labels", label_frame)
        cv.moveWindow("labels", 0,0)
        cv.moveWindow("okno pogladowe", 300,0)
        k = cv.waitKey(1)


###########                                     obsługa przycisków                         ############################################################

        if k == ord("."):               #przesuwanie do następnego labela
            if mark < len(object_list)-1:
                mark +=1
            if mark == -1:
                mark = 0

            activator = True
            adding = False

        if k == ord(","):               #przesuwanie do poprzedniego labela
            if mark > 0:
                mark -=1
            if mark == -1:
                mark = 0                
            activator = True
            adding = False
            
        if k == ord('/'):
            mark = -1
            activator = True
            adding = True
        
        if k == ord('n'):               #następne zdjęcie
            activator = True
            mark = 0
            break

        if k == ord('d'):               #usuń zdjęcie i annotacie mu odpowiadające
            os.remove(os.path.join(folder,"img",file))
            os.remove(os.path.join(folder,"label",str(file[:-4]+".txt")))
            activator = True
            mark = 0
            break
        
        if k == ord('q'):               #wyjscie z programu
            quit = True
            break

        if k == ord('r'):               #usun label
            object_list.pop(mark)
            mark = 0
            activator = True

        if k == ord('m'):
            if modyfing == False:
                modyfing = True
            else:
                modyfing = False
            
            activator = True
            labeling = False

        if k == ord('l'):
            if labeling == False:
                labeling = True
            else:
                labeling = False
            
            activator = True
            modyfing = False

        if labeling == True:
            if k == ord('1'):
                new_label = 0

                change_label(mark,new_label, object_list)

                activator = True

            if k == ord('2'):
                new_label = 1

                change_label(mark,new_label, object_list)
                
                activator = True

            if k == ord('3'):
                new_label = 2

                change_label(mark,new_label, object_list)
                
                activator = True
    
            if k == ord('4'):
                new_label = 3

                change_label(mark,new_label, object_list)
                
                activator = True

            if k == ord('5'):
                new_label = 4

                change_label(mark,new_label, object_list)
                
                activator = True

            if k == ord('6'):
                new_label = 5

                change_label(mark,new_label, object_list)

                activator = True

            if k == ord('7'):
                new_label = 6

                change_label(mark,new_label, object_list)
                
                activator = True

            if k == ord('8'):
                new_label = 7

                change_label(mark,new_label, object_list)
                
                activator = True
    
            if k == ord('9'):
                new_label = 8 

                change_label(mark,new_label, object_list)
                
                activator = True

            if k == ord('0'):
                new_label = 0

                change_label(mark,new_label, object_list)
                
                activator = True

        if modyfing == True:
            if k == ord('u'):
                
                object_list[mark] = modyfing_annotation(mark, object_list)
                activator = True

        if adding == True:              #dodawanie nowego labela
            if k == ord('1'):
                new_label = 0

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('2'):
                new_label = 1

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('3'):
                new_label = 2

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('4'):
                new_label = 3

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('5'):
                new_label = 4

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('6'):
                new_label = 5

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1


            if k == ord('7'):
                new_label = 6

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('8'):
                new_label = 7

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('9'):
                new_label = 8

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1

            if k == ord('0'):
                new_label = 9

                adding_annotation(new_label)

                
                activator = True
                adding = False
                mark = len(object_list) - 1




    if quit == True:
        break
    else:
        save_txt(os.path.join(folder,"label",str(file[:-4]+".txt")), object_list)

