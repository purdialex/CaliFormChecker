import cv2
import mediapipe as mp
from utils import get_main_body_points
from utils import is_point_in_frame

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def webcam_pose_landmarks():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)  # Use the default webcam

    with mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            static_image_mode=False,
            ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            # Draw pose landmarks on the frame and also test if keypoints move
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)
                key = cv2.waitKey(1) & 0xFF
                if key == 32:  # Spacebar
                    left_shoulder = keypoints["left_shoulder"]
                    if is_point_in_frame(left_shoulder):
                        print(" Left shoulder is in frame:", left_shoulder)
                    else:
                        print(" Left shoulder is out of frame:", left_shoulder)
            else:
                pass
            # Show the frame
            cv2.imshow("Webcam Pose Landmarks", frame)

            # Exit when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function
webcam_pose_landmarks()