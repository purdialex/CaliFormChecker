import cv2
import mediapipe as mp
from core.utils import calculate_angle, get_main_body_points
from core.pullup_checker_complex import PullUpChecker  # Your PullUpChecker class here

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def webcam_pullup_analyzer():
    checker = PullUpChecker()
    cap = cv2.VideoCapture(0)  # default webcam

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

            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                # Get keypoints dictionary from landmarks
                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)

                # Update pullup checker
                checker.update(keypoints)

                # Draw landmarks on frame
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                # Extract joints needed for angles
                l_shoulder = keypoints["left_shoulder"]
                r_shoulder = keypoints["right_shoulder"]
                l_elbow = keypoints["left_elbow"]
                r_elbow = keypoints["right_elbow"]
                l_wrist = keypoints["left_wrist"]
                r_wrist = keypoints["right_wrist"]
                l_hip = keypoints["left_hip"]
                r_hip = keypoints["right_hip"]

                # Calculate elbow angles
                left_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
                right_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

                h, w, _ = frame.shape

                # Convert normalized coords to pixels for display
                le_px = (int(l_elbow[0] * w), int(l_elbow[1] * h))
                re_px = (int(r_elbow[0] * w), int(r_elbow[1] * h))

                # Draw elbow angles
                cv2.putText(frame, f'{int(left_elbow_angle)}°', (le_px[0], le_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{int(right_elbow_angle)}°', (re_px[0], re_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

                # Display counters and feedback on top-left
                cv2.putText(frame, f'Pull-Ups: {checker.counter}', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
                cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f'Partial Pull-Ups: {checker.partial_counter}', (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

            cv2.imshow("Pull-Up Analysis", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    webcam_pullup_analyzer()
