import cv2
import numpy as np
import os
from numpy import diff

v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_3_3.mp4')
# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_mask2_nores.avi')
cap = cv2.VideoCapture(v_name)
frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# cv2.namedWindow('xd', cv2.WINDOW_FREERATIO)
colors = (
    (255, 0,   0  ), # Blue
    (255, 127, 0  ),
    (255, 255, 0  ),
    (127, 255, 0  ),
    (0,   255, 0  ), # Green
    (0,   255, 127),
    (0,   255, 255),
    (0,   127, 255),
    (0,   0,   255), # Red
    (127, 0,   255),
    (255, 0,   255),
    (255, 0,   127)
)
# 8 prostokątów
# wielkość 4x500
# image = cv2.line(image, start_point, end_point, color, thickness)


# rect_size = (100, 100)
# rect_first = (750, 450)
# rect_last = (750, 950)

def pochodna(array):
    dx = 0.1
    dy = diff(array)/dx
    return dy

rect_size = (60, 350)
rect_first = (75, 550)
rect_last = (1386, 550)
rect_count = 6
# rect_distance = int((rect_last[0] - rect_first[0]) / rect_count)
rect_distance = (int((rect_last[0] - rect_first[0]) / rect_count), int((rect_last[1] - rect_first[1]) / (rect_count - 1))) 
rectangles = []

plot_mod_x = 1
plot_mod_y = 0.5
plot_start = (75, 200)

backSub = cv2.createBackgroundSubtractorMOG2(detectShadows = False)


for i in range(rect_count):
    item = ((rect_first[0] + rect_distance[0] * i,                rect_first[1] + rect_distance[1] * i),
            (rect_first[0] + rect_distance[0] * i + rect_size[0], rect_first[1] + rect_distance[1] * i + rect_size[1]))
    rectangles.append(item)
results = [[] for i in range(int(rect_count))] 
diffs = [[] for i in range(int(rect_count))] 
diffs2 = [[] for i in range(int(rect_count))] 
frame_number = 0
ret, img = cap.read() 
fgMask = backSub.apply(img)
kernel = np.ones((3,3),np.uint8)
# fgMaskClosed = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel, iterations=3)

while ret:
    # imga = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # imgb = imga[:,:,0]
    img2 = np.dstack((fgMask, fgMask, fgMask))
    # img2 = np.dstack((fgMaskClosed, fgMaskClosed, fgMaskClosed))

    ### Rysowanie ###
    for i, rect in enumerate(rectangles):
        cv2.rectangle(img2, rect[0], rect[1], colors[i * 2], 1)

    for i, line in enumerate(results):
        # if frame_number < 2:
        if frame_number < 10:
            continue
        if i == 3:
            for j in range(frame_number - 1):
                start_point = (int(plot_start[0] + j     * plot_mod_x), -1 * int(line[j]       * plot_mod_y) + plot_start[1]) # + i * 10)
                end_point   = (int(plot_start[0] + (j+1) * plot_mod_x), -1 * int(line[j+1]     * plot_mod_y) + plot_start[1]) # + i * 10)
                cv2.line(img2, start_point, end_point, colors[0], 1)

    #         for j in range(frame_number - 2):
    #             start_diff  = (int(plot_start[0] + j     * plot_mod_x), -1 * int(diffs[i][j]   * plot_mod_y) + plot_start[1])
    #             end_diff    = (int(plot_start[0] + (j+1) * plot_mod_x), -1 * int(diffs[i][j+1] * plot_mod_y) + plot_start[1])
    #             cv2.line(img, start_diff, end_diff, colors[4], 1)

    #         # for j in range(frame_number - 3):
    #         #     start_diff2  = (int(plot_start[0] + j     * plot_mod_x), -1 * int(diffs2[i][j]   * plot_mod_y) + plot_start[1])
    #         #     end_diff2    = (int(plot_start[0] + (j+1) * plot_mod_x), -1 * int(diffs2[i][j+1] * plot_mod_y) + plot_start[1])
    #         #     cv2.line(img, start_diff2, end_diff2, colors[8], 1)

    cv2.line(img2, plot_start, (1920, plot_start[1]), (255, 255, 255), 1)

    cv2.imshow("xd", img2)
    # cv2.imshow("xdd", fgMask)
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord(' '):
        ### Generowanie danych ###
        for i, rect in enumerate(rectangles):
            check = fgMask[rect[0][1] + 1 : rect[1][1] - 1, rect[0][0] + 1 : rect[1][0] - 1] 
            val = cv2.countNonZero(check)
            # results[i].append(val)
            try:
                average = int(np.sum(check)/(rect_size[0] * rect_size[1]))
                results[i].append(average)
            except:
                # print("wtf? - ", average)
                results[i].append(0)
            # diffs[i] = pochodna(results[i])
            # diffs2[i] = pochodna(diffs[i])


        # print(results[:-1])
        ret, img = cap.read()
        fgMask = backSub.apply(img)
        # fgMaskClosed = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel, iterations=3)

        frame_number += 1
        frames_left -= 1
        if frames_left % 10 == 0:
            print(frames_left, " frames left")

cap.release()
cv2.destroyAllWindows()