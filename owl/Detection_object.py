from operator import mod
import numpy as np
import cv2

#%matplotlib inline
from matplotlib import pyplot as plt
from IPython.display import Video

np.random.seed(42)

def fixColor(image):
    if(cv2.CAP_PROP_CONVERT_RGB):
        print("Conversion BGR_to_RGB done succesfully")
    return(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def fixGray(image):
    return(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

Video("E:\Filmy\VID_20190713_210304.mp4", embed=True)

video_stream = cv2.VideoCapture('E:\Filmy\VID_20190713_210304.mp4')

# Randomly select 30 frames
frameIds = video_stream.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=30) #default: size=30 

# Store selected frames in an array
frames = []
for fid in frameIds[:10]:
    video_stream.set(cv2.CAP_PROP_POS_FRAMES, fid)
    print("CAP_PROP_POS_FRAMES", cv2.CAP_PROP_POS_FRAMES)
    ret, frame = video_stream.read()
    frames.append(frame)

video_stream.release()

# Calculate the median along the time axis
medianFrame = np.median(frames[:10], axis=0).astype(dtype=np.uint8)
plt.imshow(fixColor(medianFrame))
print("medianFrame.size:", medianFrame.shape)

# Calculate the average along the time axis
avgFrame = np.average(frames[:10], axis=1).astype(dtype=np.uint8)
plt.imshow(fixColor(avgFrame))
print("avgFrame.size:", avgFrame.shape)

sample_frame=frames[0]
plt.imshow(fixColor(sample_frame))
print("sample_frame.size:", sample_frame.shape)

grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
plt.imshow(fixColor(grayMedianFrame))
print("grayMedianFrame.size:", grayMedianFrame.shape)

graySample=cv2.cvtColor(sample_frame, cv2.COLOR_BGR2GRAY)
plt.imshow(fixColor(graySample))
print("graySample.size:", graySample.shape)

dframe = cv2.absdiff(graySample, grayMedianFrame)
plt.imshow(fixColor(dframe))
print("dframe.size:", dframe.shape)

blurred = cv2.GaussianBlur(dframe, (11,11), 0)
plt.imshow(fixColor(blurred))
print("blurred.size:", blurred.shape)

ret, tframe= cv2.threshold(blurred,10,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
plt.imshow(fixColor(tframe))
print("ret:", ret)
print("tframe: \n", tframe)
tframe = cv2.dilate(tframe, None, iterations = 2)

(cnts, _) = cv2.findContours(tframe.copy(), cv2.RETR_EXTERNAL, 
                             cv2 .CHAIN_APPROX_SIMPLE)

for cnt in cnts:
    x,y,w,h = cv2.boundingRect(cnt)
    if y > 200:  #Disregard item that are the top of the picture
        cv2.rectangle(sample_frame,(x,y),(x+w,y+h),(0,255,0),2)

plt.imshow(fixColor(sample_frame))

writer = cv2.VideoWriter("detected_video_with_changes_Parowoz.mp4", 
                         cv2.VideoWriter_fourcc(*"MP4V"), 30,(1024, 768)) #default 640x480

#Create a new video stream and get total frame count
video_stream = cv2.VideoCapture('E:\Filmy\VID_20190713_210304.mp4')
total_frames=video_stream.get(cv2.CAP_PROP_FRAME_COUNT)
print(total_frames)

frameCnt=0
while(frameCnt < total_frames):

    frameCnt+=1
    ret, frame = video_stream.read()
    wk = 2 # default value to normal detecting

    # Convert current frame to grayscale
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print("gframe.size:", gframe.shape)
    
    # Calculate absolute difference of current frame and
    # the median frame
    dframe = cv2.absdiff(gframe, grayMedianFrame)
    dframe = (dframe | (~dframe) * wk)^(2)
    dframe = cv2.erode(dframe, None, iterations = 40)
    dframe = cv2.dilate(dframe, None, iterations = 40)

    # Gaussian
    blurred = cv2.GaussianBlur(dframe, (11, 11), 0)
    
    #Thresholding to binarise
    ret, tframe= cv2.threshold(blurred,0,255,
                               cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #Identifying contours from the threshold
    (cnts, _) = cv2.findContours(tframe.copy(), 
                                 cv2.RETR_EXTERNAL, cv2 .CHAIN_APPROX_SIMPLE)
    
    #For each contour draw the bounding bos
    for cnt in cnts:
        x,y,w,h = cv2.boundingRect(cnt)
        wsp = [0, 0]
        # Disregard items in the top of the picture
        if x >= 200 & y > 0:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,100),2) 
            """
            #funkcja cv2.rectangle:
            #pierwsza wartość to odcień prostokątów do zaznaczania
            Wartość ostatnia w tym nawiasie od funkcji rectangle to wartość grubości linii
            """


        
    writer.write(cv2.resize(frame, (1024, 768))) #default: 640x480
 
#Release video object
video_stream.release()
writer.release()

                             

