import cv2 as cv
import numpy as np
 
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()         #reads camera/webcam

    img = cv.flip(frame, 1)
    width = int(cap.get(3))         #gets width for webcam
    height = int(cap.get(4))        #gets height for webcam

    #red square in top left corner
    cv.rectangle(img, (0, 0), (100, 100), (0, 0, 255), -1)  
    cv.putText(img, "RED", (0, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,0), 2, cv.LINE_AA)
    
    #green square in top right corner
    cv.rectangle(img, (width-100, 0), (width, 100), (0, 255, 0), -1)
    cv.putText(img, "GREEN", (width-100, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)    

    #blue square in bottom left corner
    cv.rectangle(img, (0, height-100), (100, height), (255, 0, 0), -1)  
    cv.putText(img, "BLUE", (0, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2, cv.LINE_AA) 

    #white square in bottom right corner
    cv.rectangle(img, (width-100, height-100), (width, height), (255, 255, 255), -1) 
    cv.putText(img, "WHITE", (width-100, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)

        

    cv.imshow('Output', img)


    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
