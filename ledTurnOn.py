import cv2 as cv
import numpy as np
import mediapipe as mp      #TODO FIX MEDIA PIPE THIS SHIT NOT WORKING!!! 
import serial   
import time


# initilalize serial communication, adjust COM port and baud rate with board 
# ser = serial.Serial(9600)
time.sleep(2)   # wait for serial to initialize 
 

cap = cv.VideoCapture(0)

# initializes hand solution

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode



while True:
    success, frame = cap.read()         #reads camera/webcam

    if not success:
        break

    img = cv.flip(frame, 1)
    width = int(cap.get(3))         #gets width for webcam
    height = int(cap.get(4))        #gets height for webcam

    rectangle_width = 100
    rectangle_height = 100 

    #red square in top left corner
    cv.rectangle(img, (0, 0), (rectangle_width,rectangle_height), (0, 0, 255), -1)  
    cv.putText(img, "RED", (0, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,0), 2, cv.LINE_AA)
    
    #green square in top right corner
    cv.rectangle(img, (width-rectangle_width, 0), (width, rectangle_height), (0, 255, 0), -1)
    cv.putText(img, "GREEN", (width-rectangle_width, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)    

    #blue square in bottom left corner
    cv.rectangle(img, (0, height-rectangle_height), (rectangle_width, height), (255, 0, 0), -1)  
    cv.putText(img, "BLUE", (0, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2, cv.LINE_AA) 

    #white square in bottom right corner
    cv.rectangle(img, (width-rectangle_width, height-rectangle_height), (width, height), (255, 255, 255), -1) 
    cv.putText(img, "WHITE", (width-rectangle_width, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)

    #processing hand landmarks

    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)    # Note: media pipes goes by blue green red, have ot covert to RGB


    cv.imshow('Output', img)


    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
