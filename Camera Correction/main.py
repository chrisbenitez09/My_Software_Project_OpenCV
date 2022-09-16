from tkinter import W
from turtle import right
from unittest import result
import cv2 as cv
import cv2
import mediapipe as mp
import numpy as np


#COLORS RGB
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
yellow = (0, 255, 255)
pink = (255, 0, 255)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#To capture a video, you need to create a VideoCapture object. Its argument can be either the device index or the name of a video file. A device index is just the number to specify which camera. Normally one camera will be connected (as in my case). So I simply pass 0 (or -1). You can select the second camera by passing 1 and so on. After that, you can capture frame-by-frame.
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print( "Can't receive frame (stream end?). Exiting ..." ) 
            break
     

        #set up color to RGB
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img.flags.writeable = False
        

        #Make detection
        result = pose.process(img)
        
        #recoloring back to BGR
        #Why recoloring : The human perception isn't built for observing fine changes in grayscale images. Human eyes are more sensitive to observing changes between colors, so you often need to recolor your grayscale images to get a clue about them.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    

        #Extract Landmarks
        try:
            landmarks = result.pose_landmarks.landmark
            
            #Shoulder and face Coordinates
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            face = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
            
        except:
            pass

        #Landmarks will detect points of our body and detected faces in images.
        mp_drawing.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
             mp_drawing.DrawingSpec(color = blue, thickness=3, circle_radius=1),
             mp_drawing.DrawingSpec(color = red, thickness=3, circle_radius=1)
        )

        # cv2.imshow() method is used to display an image in a window. The window automatically fits to the image size.
        #waitkey() function of Python OpenCV allows users to display a window for given milliseconds or until any key is pressed.
        # ord() function returns the Unicode code from a given character. This function accepts a string of unit length as an argument and returns the Unicode equivalence of the passed argument.
       
        cv.imshow('VideoPosture', img)
        if cv.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows() #destroyAllWindows() function allows users to destroy or close all windows at any time after exiting the script