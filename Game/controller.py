import cv2
import mediapipe as mp
import time, sys

def controller_thread(controller_state: list):
    mp_pose = mp.solutions.pose

    # For webcam input:
    cap = cv2.VideoCapture(1)

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            res, image = cap.read()
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            width = image.shape[1]

            # Cut the image in half
            width_cutoff = width // 2
            s1 = image[:, :width_cutoff]
            s2 = image[:, width_cutoff:]

            results_1 = pose.process(s1)
            results_2 = pose.process(s2)


            if results_1.pose_landmarks != None and results_1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].z < -1.8 and results_1.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y > 0.6:
                controller_state[0] = True	
            else:
                controller_state[0] = False

            if results_2.pose_landmarks != None and results_2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].z < -1.8 and results_2.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y > 0.6:
                controller_state[1] = True
            else:
                controller_state[1] = False
            

    cap.release()
