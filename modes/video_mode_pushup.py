import cv2
import mediapipe as mp
from core.pushup_checker_complex import PushupChecker
from core.utils import get_main_body_points, calculate_angle

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def video_pose_landmarks(input_video_path, output_video_path):
    # Open input video
    checker = PushupChecker()
    cap = cv2.VideoCapture(input_video_path)  # ✅ Fixed: removed second argument
    rotation_code = None

    try:
        # Check for rotation metadata (common in mobile videos) and flip if needed
        rotation = int(cap.get(cv2.CAP_PROP_ORIENTATION_META))
        if rotation == 180:
            rotation_code = cv2.ROTATE_180
        elif rotation == 90:
            rotation_code = cv2.ROTATE_90_CLOCKWISE
        elif rotation == 270:
            rotation_code = cv2.ROTATE_90_COUNTERCLOCKWISE
    except:
        pass

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video details
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create VideoWriter for output
    #fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    with mp_pose.Pose(
        model_complexity=1,
        static_image_mode=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Handle rotation
            if rotation_code is not None:
                frame = cv2.rotate(frame, rotation_code)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                checker.update(results.pose_landmarks, mp_pose)

                # Draw pose landmarks
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Feedback display
                cv2.putText(frame, f'Perf Pushups: {checker.counter}', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if checker.feedback == "LOCKOUT BETTER!":
                    cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 5)
                cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cv2.putText(frame, f'Midway Pushups: {checker.partial_counter}', (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)

                # Extract joints
                left_shoulder = keypoints["left_shoulder"]
                left_elbow = keypoints["left_elbow"]
                left_wrist = keypoints["left_wrist"]
                right_shoulder = keypoints["right_shoulder"]
                right_elbow = keypoints["right_elbow"]
                right_wrist = keypoints["right_wrist"]
                left_hip = keypoints["left_hip"]
                left_knee = keypoints["left_knee"]
                left_ankle = keypoints["left_ankle"]
                right_hip = keypoints["right_hip"]
                right_knee = keypoints["right_knee"]
                right_ankle = keypoints["right_ankle"]

                # Compute angles
                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_torso_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_torso_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                h, w, _ = frame.shape

                le_px = int(left_elbow[0] * w), int(left_elbow[1] * h)
                re_px = int(right_elbow[0] * w), int(right_elbow[1] * h)
                lk_px = int(left_knee[0] * w), int(left_knee[1] * h)
                rk_px = int(right_knee[0] * w), int(right_knee[1] * h)
                lh_px = int(left_hip[0] * w), int(left_hip[1] * h)
                rh_px = int(right_hip[0] * w), int(right_hip[1] * h)

                cv2.putText(frame, f'{int(left_arm_angle)}', (le_px[0], le_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
                cv2.putText(frame, f'{int(right_arm_angle)}', (re_px[0], re_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)
                cv2.putText(frame, f'{int(left_leg_angle)}', (lk_px[0], lk_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                cv2.putText(frame, f'{int(right_leg_angle)}', (rk_px[0], rk_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                cv2.putText(frame, f'{int(left_torso_angle)}', (lh_px[0], lh_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)
                cv2.putText(frame, f'{int(right_torso_angle)}', (rh_px[0], rh_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)

            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

# Uncomment this block only if using from command line:
"""
input_path = input("Enter path of the input video: ")
output_path = input("Enter output video path (e.g., output.mp4): ")
video_pose_landmarks(input_path, output_path)
"""
