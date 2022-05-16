"""
Program do tworzenia zbiorów do nauki z renderu z blendera. W planach zmiana z domyślej jednej klasy, na klasy zależne od koloru. 

Plik do poprawnego działania potrzebuje mieć obok siebie folder "Data" i w nim folder z podfolderami "boxes" i "img". Zawierające zdjęcia z nazwami kompatybilnymi nazwami
składającymi się z litery I lub M kolejno dla zdjęć lub boxów, i numeru dopełnionego zerami do 4 cyfr. 

Efektem pracy programu jest
  -folder "results" z trzema podfolderami "test", "train", "valid", gdzie w każdym znajdują się dwa podfodery "images" i "labels" zawierające kolejno zdjęcia
   i annotacie opisujące położenie interesującego nas obiektu w formacie yolo (label, center_x, center_y, with, height) przy czym infromacje te są zapisywane
   w postaci (wartość / maksymalna_wartość_dla_zdjecia np. center_x = położenie_srodka_obiektu_w_osi_x_w_pixelach / cała_szerokość_obrazu).
  -plikiem "data.yaml" zawierający listę labeli, ilość labeli, ścieżki do folderu ze zdjęciami do treningu i validacji. 
  -gdy debug = True, zdjęcie "result_with_boxes.jpg" pokazujące ostatni wynik pracy programu.

Położenie oryginału: /home/mbak/Yolo5/dataset_creator_from_box.py
"""
from posixpath import dirname
import string
import cv2 as cv
import numpy
import os

name_of_folder = "owl"    #Nazwa folderu w folderze Data z którego zostaną odczytane dane i zapisany resultat prac
img_list = [] 
box_list = []
checked_elements_list = []  
debug = True              #Gdy True program zapisze w folderze 
TVT_ratio = [70,20,10]          #wspołczynnik odpowiedzialny za podział zdjęć na train, valid, test w odpowiednich proporcjach 
                                # SUMA MUSI WYNOSIC 100, zalecane 70,20,10

    #pobranie nazw plików
for img in os.listdir(os.path.join("Data", name_of_folder, "img")):
    img_list.append(img)
for box in os.listdir(os.path.join("Data", name_of_folder, "boxes")):
    box_list.append(box)   


    #sprawdzenie czy pliki są kompatybilne (mają parę)
for box in box_list:
    if "I"+str(box[1:]) in img_list:
        checked_elements_list.append(box[1:])
    
print(box_list)
print(checked_elements_list)



dirName = os.path.join("Data", name_of_folder, "results")
    
# Create target directory & all intermediate directories if don't exists
try:
    os.makedirs(dirName)    
    print("Directory " , dirName ,  " Created ")
    
except FileExistsError:
    print("Directory " , dirName ,  " already exists")  


annotation_dict = {}
for element in checked_elements_list:
    print(element)
    box = cv.imread(os.path.join("Data", name_of_folder, "boxes",str("M"+element)))
    
    box_h, box_w, box_ch = box.shape

    box_gray = cv.cvtColor(box, cv.COLOR_BGR2GRAY)
    

    ###### Odnajdywanie boxów na obrazku
    ret, thresh = cv.threshold(box_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)     #odczytaj kontury
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    max_x =[]
    max_y =[]
    min_x =[]
    min_y =[]
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
        cv.rectangle(box, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), (0,255,0), 2)
        if min_x == []:
            min_x = boundRect[i][0]
        else:
            if min_x > boundRect[i][0]:
                min_x = boundRect[i][0]
        if min_y == []:
            min_y = boundRect[i][1]
        else:
            if min_y > boundRect[i][1]:
                min_y = boundRect[i][1]
        if max_x == []:
            max_x = boundRect[i][0]+boundRect[i][2]
        else:
            if max_x < boundRect[i][0]+boundRect[i][2]:
                max_x = boundRect[i][0]+boundRect[i][2]
        if max_y == []:
            max_y = boundRect[i][1]+boundRect[i][3]
        else:
            if max_y < boundRect[i][1]+boundRect[i][3]:
                max_y = boundRect[i][1]+boundRect[i][3]
    
    ######## zmiena na wartość 0-1
    center_x = 0
    center_y = 0
    width = 0
    height = 0

    center_x = ((max_x + min_x)/2)/box_w
    center_y = ((max_y + min_y)/2)/box_h
    width = (max_x-min_x)/box_w
    height = (max_y - min_y)/box_h
    
    # if min_x != 0 and max_x !=0 and min_y != 0 and max_y != 0:
    annotation_dict[element] = (0,center_x,center_y,width,height)

    ######## Wyswietlanie ostatniego zdjecia    
if debug:
    cv.rectangle(box, (int(min_x), int(min_y)), \
        (int(max_x), int(max_y)), (0,255,255), 2)
    cv.circle(box, (int(center_x),int(center_y)), 5,(255,0,0),-1)
    cv.imwrite(os.path.join("Data", name_of_folder, "results", "result_with_boxes.jpg"), box)
    print(annotation_dict)


 ### podział na train, valid, test
for name in ["train", "valid", "test"]:
    dirName = os.path.join("Data", name_of_folder, "results", name)
    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(dirName)    
        print("Directory " , dirName ,  " Created ")
        for name_2 in ["images", "labels"]:
            dirName = os.path.join("Data", name_of_folder, "results", name, name_2)
            try:
                os.makedirs(dirName)
                print("Directory " , dirName ,  " Created ")
            except FileExistsError:
                print("Directory " , dirName ,  " already exists")    
    except FileExistsError:
        print("Directory " , dirName ,  " already exists") 
        for name_2 in ["images", "labels"]:
            dirName = os.path.join("Data", name_of_folder, "results", name, name_2)
            try:
                os.makedirs(dirName)
                print("Directory " , dirName ,  " Created ")
            except FileExistsError:
                print("Directory " , dirName ,  " already exists")    

train_len = round(len(checked_elements_list)*TVT_ratio[0]/100)
valid_len = round(len(checked_elements_list)*TVT_ratio[1]/100)
test_len = round(len(checked_elements_list)*TVT_ratio[2]/100)

print(train_len)
print(valid_len)
print(test_len)

################# Zapis wyników do odpowiednich folderów ################

for count, element in enumerate(checked_elements_list):
    img = cv.imread(os.path.join("Data", name_of_folder, "img",str("I"+element)))
    annotation = annotation_dict[element]
    if count < train_len:
        cv.imwrite(os.path.join("Data", name_of_folder, "results", "train", "images", str("I"+element)), img)
        file = open(os.path.join("Data", name_of_folder, "results", "train", "labels",str("I"+element[:-4]+".txt")), 'w')
        file.write(f"{annotation[0]} {annotation[1]} {annotation[2]} {annotation[3]} {annotation[4]}")
        file.close()
    if count < train_len+valid_len and count > train_len:
        cv.imwrite(os.path.join("Data", name_of_folder, "results", "valid", "images", str("I"+element)), img)
        file = open(os.path.join("Data", name_of_folder, "results", "valid", "labels",str("I"+element[:-4]+".txt")), 'w')
        file.write(f"{annotation[0]} {annotation[1]} {annotation[2]} {annotation[3]} {annotation[4]}")
        file.close()
    if count < train_len+valid_len+test_len and count > train_len+valid_len:
        cv.imwrite(os.path.join("Data", name_of_folder, "results", "test", "images", str("I"+element)), img)
        file = open(os.path.join("Data", name_of_folder, "results", "test", "labels",str("I"+element[:-4]+".txt")), 'w')
        file.write(f"{annotation[0]} {annotation[1]} {annotation[2]} {annotation[3]} {annotation[4]}")
        file.close()
