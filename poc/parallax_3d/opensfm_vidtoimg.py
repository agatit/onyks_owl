import os
import cv2

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_mask_nores.avi')
dir_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'photo/out_2_39_masked')
cap = cv2.VideoCapture(v_name)
# TODO tworzenie nieistniejącego directory
ret, img = cap.read()
img_num = 0
while ret:
    file_name = '%s/%s.jpg' % (dir_name , str(img_num).zfill(3))
    
    # f_name = os.path.join(dir_name,file_name) 
    if img_num % 10 == 0:
        cv2.imwrite(file_name, img)
        print(img_num)
    img_num += 1
    ret, img = cap.read()

# TODO wrzucić pierwszy materiał zZBUFFERowany