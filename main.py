import cv2
import mediapipe as mp
from utils import calculate_angle, get_coords, is_angle_within_range

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

        # Get key points
        shoulder = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        elbow = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
        wrist = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        hip = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        ankle = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)

        # Calculate angles
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        body_angle = calculate_angle(shoulder, hip, ankle)

        # Check form
        good_elbow = elbow_angle > 165  # Straight arms
        good_body = is_angle_within_range(body_angle, 180, tolerance=15)  # Horizontal line

        if good_elbow and good_body:
            print(f"[Frame {frame_count}] ✅ Good front lever")
        else:
            print(f"[Frame {frame_count}] ❌ Fix form - Elbow: {elbow_angle:.1f}, Body: {body_angle:.1f}")

cap.release()
