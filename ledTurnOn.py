import cv2 as cv
import numpy as np
import mediapipe as mp      #TODO FIX MEDIA PIPE THIS SHIT NOT WORKING!!! 
from mediapipe import solutions
import serial
import time


# initilalize serial communication, adjust COM port and baud rate with board 
# ser = serial.Serial(9600)
time.sleep(2)   # wait for serial to initialize 
 

cap = cv.VideoCapture(0)

# initializes hand solution
handSolution = mp.solutions.hands 
hands = handSolution.Hands() 
mp_drawing = mp.solutions.drawing_utils



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
    recordHands = hands.process(img_rgb)

    if recordHands.multi_hand_landmarks:     #detects if there are any hands in the frame
        for hand_landmarks in recordHands.multi_hand_landmarks:     #iterates throguh each detected hand 

            # landmark 8 is the position of the index finger 
            x = int(hand_landmarks.landmark[8].x * width)   
            y = int(hand_landmarks.landmark[8].y * height)

            #initialize RGB values 
            red, green, blue = 0 ,0 ,0
            
            # check if index is in the red rectangle
            if 0 <= x <= width and 0 <= y <= height:
                red = 255 
                rgb_message = f"{red}, {green}, {blue}\n"
                # ser.write(rgb_message.encode())     #sends message to arduino
                print("Red zone detected")


            

    cv.imshow('Output', img)


    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
