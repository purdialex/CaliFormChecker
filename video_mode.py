import cv2
import mediapipe as mp
import os
# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def video_pose_landmarks(input_video_path, output_video_path):
    # Open input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    # Get video details (frame width, height, and frames per second)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # Create VideoWriter object for saving output video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    with mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 0)
            # Convert frame to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            # Draw pose landmarks on the frame
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                pass
            # Write the frame with landmarks to the output video
            out.write(frame)

        # Release everything when done
        cap.release()
        out.release()
        cv2.destroyAllWindows()

# Call the function with your video path and desired output path

input_path = input("please enter the path of the video you want to pose landmark")
input_video = input_path
print(f"Input video path: {input_video}")

output_path = input("please enter the path of the directory + the desired filename in .avi or .mp4 extension")
output_video =   output_path


video_pose_landmarks(input_video, output_video)
