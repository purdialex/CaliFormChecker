import cv2
import mediapipe as mp

# Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Path to your video
video_path = "D:\\Descarcari\frontlever_test.mp4"  # Change this to your actual filename
cap = cv2.VideoCapture(video_path)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Convert image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
cap.release()
