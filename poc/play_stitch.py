import os
import rectify
import cv2
import json
import numpy as np
from speed import CarSpeedEstimator
from stitch import CarStitcherFullFrame, CarStitcherRoi, CarStitcherDelayed
from deblur import Deblur

show_scale = 1

pause = False
video_path = 'samples/choiny2022/gora/6.mp4'
path, filename = os.path.split(os.path.abspath(video_path))
basename, extension = os.path.splitext(filename)

with open("samples/choiny2022/gora/gora.json") as f:
    rectify.calc_maps(json.load(f), 1920, 1080)

cap = cv2.VideoCapture(video_path)
 
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

frame_size = (1920,1080)
motion_roi = (200,300,200,100) #300:-100,500:-500 # motion_roi[1]:-motion_roi[3],motion_roi[0]:-motion_roi[2]
stich_roi = (1100,0,400,0)

meter = CarSpeedEstimator()
# stitcher = CarStitcherDelayed(roi_size=stich_roi, delay=50)
stitcher = CarStitcherRoi(roi_size=stich_roi)
deblur = Deblur(51)
deblur.set_speed(120, 0, 1, 1.2)

frame_no = 0

while(cap.isOpened()):

  frame_no += 1
  
  ret, frame = cap.read()

  if ret == True:
   
    # prespektywa
    rectified = rectify.rectify(frame)

    # usunięcie rozmycia
    # rectified = deblur.next(rectified)

    # crop
    # cropped = rectified[300:-100,500:-500]
    cropped = rectified[motion_roi[1]:-motion_roi[3],motion_roi[0]:-motion_roi[2]]

    # pomiar prędkości
    debug = np.zeros_like(cropped)
    velocity, debug = meter.next(cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY), debug=debug)
    print(f"velocity={velocity}")
    cropped = cv2.add(cropped,debug)
    
    # sklejanie
    result = stitcher.next(rectified, velocity)

    # wyświetlanie :)
    if result is not None:
      areas = np.zeros_like(result)
      areas = cv2.rectangle(areas, (motion_roi[0],motion_roi[1]), (frame_size[0]-motion_roi[2],frame_size[1]-motion_roi[3]), (255,0,0), 1)
      areas = cv2.rectangle(areas, (stich_roi[0],stich_roi[1]), (frame_size[0]-stich_roi[2],frame_size[1]-stich_roi[3]), (0,255,0), 1)      
      result = cv2.add(result, areas)
      result = cv2.resize(result, (int(result.shape[1]*show_scale), int(result.shape[0]*show_scale)))
      cv2.imshow('result',result)

    cropped = cv2.resize(cropped, (int(cropped.shape[1]*show_scale), int(cropped.shape[0]*show_scale)))    
    cv2.imshow('cropped',cropped)

    if pause:
      c = cv2.waitKey(-1)
    else:
      c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
      break
    if c & 0xFF == ord('s'):
      cv2.imwrite(os.path.join(path, f"{basename}_{frame_no}.png"), rectified)
    elif c & 0xFF == ord(' '):
      pause = not pause

  else: 
    break

cap.release()
cv2.destroyAllWindows()