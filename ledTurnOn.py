import cv2 as cv
import numpy as np
 
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()         #reads camera/webcam
    width = int(cap.get(3))         #gets width for webcam
    height = int(cap.get(4))        #gets height for webcam

    img = cv.rectangle(frame, (100, 100), (200, 200), (0, 0, 255), -1)    
    img = cv.rectangle(frame, (400, 100), (500, 200), (0, 0, 0), -1)    

    cv.imshow('frame', img)


    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
