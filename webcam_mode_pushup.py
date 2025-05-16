import cv2
import mediapipe as mp
from pushup_checker_simple import PushupChecker
from utils import get_main_body_points, calculate_angle

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def webcam_pose_landmarks():
    # Initialize the webcam and pushup checker
    checker = PushupChecker()
    cap = cv2.VideoCapture(0)  # Use the default webcam

    with mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            static_image_mode=False
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                # Update pushup checker
                checker.update(results.pose_landmarks, mp_pose)

                # Draw pose landmarks
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

                # Get all keypoints
                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)

                # Extract all joints
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

                # Calculate all angles
                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_torso_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_torso_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                # Convert normalized coordinates to pixel values
                h, w, _ = frame.shape

                # Arm angles at elbows
                le_px = int(left_elbow[0] * w), int(left_elbow[1] * h)
                re_px = int(right_elbow[0] * w), int(right_elbow[1] * h)

                # Leg angles at knees
                lk_px = int(left_knee[0] * w), int(left_knee[1] * h)
                rk_px = int(right_knee[0] * w), int(right_knee[1] * h)

                # Torso angles at hips
                lh_px = int(left_hip[0] * w), int(left_hip[1] * h)
                rh_px = int(right_hip[0] * w), int(right_hip[1] * h)

                # Draw all angles on frame with different colors
                # Arm angles (blue)
                cv2.putText(frame, f'{int(left_arm_angle)}°', (le_px[0], le_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{int(right_arm_angle)}°', (re_px[0], re_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

                # Leg angles (red)
                cv2.putText(frame, f'{int(left_leg_angle)}°', (lk_px[0], lk_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{int(right_leg_angle)}°', (rk_px[0], rk_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                # Torso angles (yellow)
                cv2.putText(frame, f'{int(left_torso_angle)}°', (lh_px[0], lh_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{int(right_torso_angle)}°', (rh_px[0], rh_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

                # Display counter and feedback (top left)
                cv2.putText(frame, f'Pushups: {checker.counter}', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

            # Show the frame
            cv2.imshow("Pushup Analysis", frame)

            # Exit when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

webcam_pose_landmarks()