import cv2 as cv
import mediapipe as mp
import time
import serial

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

#intializing serial communication 
# ser = serial.Serial('/dev/cu.usbserial-210', 9600)  # Adjust the port name as needed
time.sleep(2)   # wait for serial to initialize')

# Global variable to store the latest result
latest_result = None
lastPrintTime = 0

def colored_squares():
        #red square in top left corner
    cv.rectangle(frame, (0, 0), (rectangle_width,rectangle_height), (0, 0, 255), -1)  
    
    #green square in top right corner
    cv.rectangle(frame, (width-rectangle_width, 0), (width, rectangle_height), (0, 255, 0), -1)

    #blue square in bottom left corner
    cv.rectangle(frame, (0, height-rectangle_height), (rectangle_width, height), (255, 0, 0), -1)  

    #white square in bottom right corner
    cv.rectangle(frame, (width-rectangle_width, height-rectangle_height), (width, height), (255, 255, 255), -1) 

def text_on_squares():
        #text in red square in top left corner
    cv.putText(frame, "RED", (0, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,0), 2, cv.LINE_AA)
    
    #text in green square in top right corner
    cv.putText(frame, "GREEN", (width-rectangle_width, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)    

    #text in blue square in bottom left corner
    cv.putText(frame, "BLUE", (0, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2, cv.LINE_AA) 

    #text in white square in bottom right corner
    cv.putText(frame, "WHITE", (width-rectangle_width, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)


def zone_detection(): 
            # Convert normalized coordinates to pixel coordinates
    x = int((1.0 - landmark.x)* frame.shape[1])
    y = int(landmark.y * frame.shape[0])
    # points = cv.circle(frame, (x, y), 5, (0, 255, 0), -1)

    red, green, blue = 0, 0, 0 

    if 0 <= x <= rectangle_width and 0 <= y <= rectangle_height: 
        red = 255
        rgb_message = f"{red},{green},{blue}"
        # ser.write(rgb_message.encode())
        print("RED Zone Detected")

    elif (width - rectangle_width) <= x <= width and 0 <= y <= rectangle_height:
        green = 255
        rgb_message = f"{red},{green},{blue}"
        # ser.write(rgb_message.encode())
        print("GREEN Zone Detected")

    elif 0 <= x <= rectangle_width and (height - rectangle_height) <= y <= height:
        blue = 255
        rgb_message = f"{red},{green},{blue}"
        # ser.write(rgb_message.encode())
        print("BLUE Zone Detected")

    elif (width - rectangle_width) <= x <= width and (height - rectangle_height) <= y <= height:
        white = 255
        rgb_message = f"{red},{green},{blue}"
        # ser.write(rgb_message.encode())
        print("WHITE Zone Detected")
     

# Callback function for live stream mode
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result, lastPrintTime

    currentTime = time.time() 

    latest_result = result

    if result.hand_landmarks and (currentTime - lastPrintTime) >= 1.0:
        print(f'Detected {len(result.hand_landmarks)} hand(s) at timestamp: {timestamp_ms}ms')
        lastPrintTime = currentTime

# Configure the hand landmarker
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,  # Detect up to 2 hands
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    result_callback=print_result)




# Initialize webcam
cap = cv.VideoCapture(0)

# Create the hand landmarker
with HandLandmarker.create_from_options(options) as landmarker:
    frame_timestamp_ms = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert BGR to RGB (MediaPipe uses RGB)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        # Convert to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Send frame to landmarker asynchronously
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        frame = cv.flip(frame, 1)
        width = int(cap.get(3))         #gets width for webcam
        height = int(cap.get(4))        #gets height for webcam

        rectangle_width = 100
        rectangle_height = 100 

        colored_squares()
        text_on_squares()
        
        # Draw landmarks if available
        if latest_result and latest_result.hand_landmarks:
            for hand_landmarks in latest_result.hand_landmarks:
                # Draw each landmark
                for landmark in hand_landmarks:
                    # Convert normalized coordinates to pixel coordinates
                   zone_detection()

                
                
                # You need to create a temporary image for drawing
                annotated_frame = frame.copy()
        
        # Display FPS
        cv.putText(frame, f'Hands detected: {len(latest_result.hand_landmarks) if latest_result and latest_result.hand_landmarks else 0}', 
                    (150, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show the frame
        cv.imshow('Hand Tracking', frame)
        
        # Increment timestamp (in milliseconds)
        frame_timestamp_ms += 33  # Approximately 30 fps
        
        # Break on 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
cv.destroyAllWindows()