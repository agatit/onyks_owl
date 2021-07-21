import cv2
import numpy as np
import os

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_mask_nores.avi')
# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_mask2_nores.avi')
cap = cv2.VideoCapture(v_name)
frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# keyPoints = (
#              (25, 275),
#              (27, 107),
#              (462, 119),
#              (463, 240)
#              )

# rectangles = (
#     ((75, 321),(78, 825)),
#     ((1386, 357),(1389, 720))
# )
colors = (
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (127, 255, 0),
    (0, 255, 0),
    (0, 255, 127),
    (0, 255, 255),
    (0, 127, 255)
)
# 8 prostokątów
# wielkość 4x500
# image = cv2.line(image, start_point, end_point, color, thickness)


rect_size = (10, 200)
rect_first = (75, 300)
rect_last = (1386, 300)
rect_count = 8
rect_distance = int((rect_last[0] - rect_first[0]) / rect_count)
rectangles = []

plot_mod_x = 3
plot_mod_y = 0.5
plot_start = (75, 200)

for i in range(rect_count):
    item = ((rect_first[0] + rect_distance * i, rect_first[1]), (rect_first[0] + rect_distance * i + rect_size[0], rect_first[1] + rect_size[1]))
    rectangles.append(item)
# TODO interesting...   To teraz jeszcze z przesuwaniem w osi Y
results = [[] for i in range(int(rect_count))] 
frame_number = 0
ret, img = cap.read() 
while ret:
    imgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ### Rysowanie ###
    for i, rect in enumerate(rectangles):
        cv2.rectangle(img, rect[0], rect[1], colors[i], 1)

    for i, line in enumerate(results):
        if frame_number < 2:
            continue
        if i == 3:
            for j in range(frame_number - 1):
                start_point = (int(plot_start[0] + j * plot_mod_x), int(line[j] * plot_mod_y))
                end_point = (int(plot_start[0] + (j+1) * plot_mod_x), int(line[j+1] * plot_mod_y))
                cv2.line(img, start_point, end_point, colors[i], 1)


    cv2.imshow("xd", img)
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('e'):
        ### Generowanie danych ###
        for i, rect in enumerate(rectangles):
            check = imgb[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]] 
            val = cv2.countNonZero(check)
            # results[i].append(val)
            try:
                average = int(np.sum(check)/(rect_size[0] * rect_size[1]))
                results[i].append(average)
            except:
                # print("wtf? - ", average)
                results[i].append(0)
                

        # print(results[:-1])
        ret, img = cap.read()
        frame_number += 1
        frames_left -= 1
        if frames_left % 10 == 0:
            print(frames_left, " frames left")

cap.release()
cv2.destroyAllWindows()