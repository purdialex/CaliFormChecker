import cv2
import mediapipe as mp
from streamlit_webrtc import VideoProcessorBase
from core.pushup_checker_complex import PushupChecker
from core.utils import get_main_body_points, draw_angle

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class PushupCameraProcessor(VideoProcessorBase):
    def __init__(self):
        self.pose = mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.checker = PushupChecker()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            self.checker.update(results.pose_landmarks, mp_pose)
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            keypoints = get_main_body_points(results.pose_landmarks, mp_pose)
            h, w, _ = img.shape

            draw_angle(img, "left_arm", keypoints["left_shoulder"], keypoints["left_elbow"], keypoints["left_wrist"], (255, 0, 0), h, w)
            draw_angle(img, "right_arm", keypoints["right_shoulder"], keypoints["right_elbow"], keypoints["right_wrist"], (255, 0, 0), h, w)
            draw_angle(img, "left_leg", keypoints["left_hip"], keypoints["left_knee"], keypoints["left_ankle"], (0, 0, 255), h, w)
            draw_angle(img, "right_leg", keypoints["right_hip"], keypoints["right_knee"], keypoints["right_ankle"], (0, 0, 255), h, w)
            draw_angle(img, "left_torso", keypoints["left_shoulder"], keypoints["left_hip"], keypoints["left_knee"], (0, 255, 255), h, w)
            draw_angle(img, "right_torso", keypoints["right_shoulder"], keypoints["right_hip"], keypoints["right_knee"], (0, 255, 255), h, w)

            # Display feedback and counters
            cv2.putText(img, f'Perf Pushups: {self.checker.counter}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if self.checker.feedback == "LOCKOUT BETTER!":
                cv2.putText(img, f'Feedback: {self.checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5)

            cv2.putText(img, f'Feedback: {self.checker.feedback}', (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            cv2.putText(img, f'Midway Pushups: {self.checker.partial_counter}', (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return frame.from_ndarray(img, format="bgr24")
