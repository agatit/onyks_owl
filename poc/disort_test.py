import cv2 as cv
import numpy as np

scale = 2

vid = cv.VideoCapture("rtsp://admin:Kartofel_1410@192.168.1.44:554")
ret, frame = vid.read()

image_shape = np.shape(frame)
print(image_shape)
  
while(ret):
    ret, frame = vid.read()
    frame = cv.resize(frame, (image_shape[1]//scale,image_shape[0]//scale))
    cv.imshow('frame', frame)
      
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()