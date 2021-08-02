import cv2
import os
import numpy as np


v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_3_3.mp4')
cap = cv2.VideoCapture(v_name)

ret, img = cap.read() 

windowSize = (img.shape[1], img.shape[0])
out_name = v_name[:-4] + '_sharp' + '.avi'
out_fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_framerate = cap.get(cv2.CAP_PROP_FPS)
out_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0] * 2, windowSize[1] * 2))
out_out = cv2.VideoWriter(out_name, out_fourcc, out_framerate, (windowSize[0], windowSize[1]))

frames_left = cap.get(cv2.CAP_PROP_FRAME_COUNT)


while ret:
    gaussian_3 = cv2.GaussianBlur(img, (0, 0), 2.0)
    unsharp_image = cv2.addWeighted(img, 1.5, gaussian_3, -0.5, 0, img)

    cv2.imshow('img', img)
    cv2.imshow('dst', unsharp_image)

    out_out.write(unsharp_image)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    ret, img = cap.read() 

    frames_left -= 1
    if frames_left % 10 == 0:
        print(frames_left, " frames left")


out_out.release()
cap.release()
cv2.destroyAllWindows()

#TODO fuck it