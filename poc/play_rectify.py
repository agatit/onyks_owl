
import rectify
import cv2
import json
import numpy as np

with open("../samples/choiny2022/gora/gora.json") as f:
    rectify.calc_maps(json.load(f), 1920, 1080)

cap = cv2.VideoCapture('../samples/choiny2022/gora/1.mp4')
 
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
while(cap.isOpened()):
 
  ret, frame = cap.read()
  if ret == True:
 
    frame = rectify.rectify(frame)
    cv2.imshow('Frame',frame)
    
 
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else: 
    break

cap.release()
cv2.destroyAllWindows()