import cv2 as cv
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Global variable to store the latest result
latest_result = None

# Callback function for live stream mode
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result
    # Optionally print the result
    if result.hand_landmarks:
        print(f'Detected {len(result.hand_landmarks)} hand(s) at timestamp: {timestamp_ms}ms')

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

        #red square in top left corner
        cv.rectangle(frame, (0, 0), (rectangle_width,rectangle_height), (0, 0, 255), -1)  
        cv.putText(frame, "RED", (0, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,0), 2, cv.LINE_AA)
        
        #green square in top right corner
        cv.rectangle(frame, (width-rectangle_width, 0), (width, rectangle_height), (0, 255, 0), -1)
        cv.putText(frame, "GREEN", (width-rectangle_width, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)    

        #blue square in bottom left corner
        cv.rectangle(frame, (0, height-rectangle_height), (rectangle_width, height), (255, 0, 0), -1)  
        cv.putText(frame, "BLUE", (0, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0), 2, cv.LINE_AA) 
        #white square in bottom right corner
        cv.rectangle(frame, (width-rectangle_width, height-rectangle_height), (width, height), (255, 255, 255), -1) 
        cv.putText(frame, "WHITE", (width-rectangle_width, height-50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0,0,0), 2, cv.LINE_AA)
        
        # Draw landmarks if available
        if latest_result and latest_result.hand_landmarks:
            for hand_landmarks in latest_result.hand_landmarks:
                # Draw each landmark
                for landmark in hand_landmarks:
                    # Convert normalized coordinates to pixel coordinates
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    points = cv.circle(frame, (x, y), 5, (0, 255, 0), -1)
                    cv.flip(points, 1)
                
                
                # You need to create a temporary image for drawing
                annotated_frame = frame.copy()
                
                # # Draw hand landmarks on the frame
                # for idx, hand_landmarks_proto in enumerate(latest_result.hand_landmarks):
                #     # Convert to the format drawing_utils expects
                #     hand_landmarks_drawing = mp_hands.HandLandmark
                    
                #     # Create landmark list
                #     landmarks_list = []
                #     for landmark in hand_landmarks_proto:
                #         landmarks_list.append(landmark)
        
        # Display FPS
        cv.putText(frame, f'Hands detected: {len(latest_result.hand_landmarks) if latest_result and latest_result.hand_landmarks else 0}', 
                    (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
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