import cv2
import mediapipe as mp

from pushup_checker import PushupChecker
from utils import get_main_body_points, calculate_angle
from utils import is_point_in_frame

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def webcam_pose_landmarks():
    # Initialize the webcam
    checker = PushupChecker()

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

            # Draw pose landmarks on the frame
            if results.pose_landmarks:
                checker.update(results.pose_landmarks, mp_pose)

                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)

                # Extract points
                ls = keypoints["left_shoulder"]
                le = keypoints["left_elbow"]
                lw = keypoints["left_wrist"]

                rs = keypoints["right_shoulder"]
                re = keypoints["right_elbow"]
                rw = keypoints["right_wrist"]

                # Calculate angles
                l_angle = calculate_angle(ls, le, lw)
                r_angle = calculate_angle(rs, re, rw)

                # Convert normalized elbow positions to pixel coordinates
                h, w, _ = frame.shape
                le_px = int(le[0] * w), int(le[1] * h)
                re_px = int(re[0] * w), int(re[1] * h)

                # Draw angles on elbows
                cv2.putText(frame, f'{int(l_angle)}', (le_px[0], le_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{int(r_angle)}', (re_px[0], re_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Pushups: {checker.counter}', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

            # Show the frame
            cv2.imshow("Webcam Pose Landmarks", frame)

            # Exit when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Run it
webcam_pose_landmarks()
