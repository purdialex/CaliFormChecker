import cv2
import mediapipe as mp
from streamlit_webrtc import VideoProcessorBase
from core.pushup_checker_complex import PushupChecker
from core.utils import get_main_body_points, calculate_angle

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
            mp_drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            keypoints = get_main_body_points(results.pose_landmarks, mp_pose)
            h, w, _ = img.shape


            def draw_angle(name, pt1, pt2, pt3, color):
                angle = calculate_angle(pt1, pt2, pt3)
                px = int(pt2[0] * w), int(pt2[1] * h)
                cv2.putText(img, f'{int(angle)}°', (px[0], px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

            draw_angle("left_arm", keypoints["left_shoulder"], keypoints["left_elbow"], keypoints["left_wrist"], (255, 0, 0))
            draw_angle("right_arm", keypoints["right_shoulder"], keypoints["right_elbow"], keypoints["right_wrist"], (255, 0, 0))
            draw_angle("left_leg", keypoints["left_hip"], keypoints["left_knee"], keypoints["left_ankle"], (0, 0, 255))
            draw_angle("right_leg", keypoints["right_hip"], keypoints["right_knee"], keypoints["right_ankle"], (0, 0, 255))
            draw_angle("left_torso", keypoints["left_shoulder"], keypoints["left_hip"], keypoints["left_knee"], (0, 255, 255))
            draw_angle("right_torso", keypoints["right_shoulder"], keypoints["right_hip"], keypoints["right_knee"], (0, 255, 255))

            cv2.putText(img, f'Pushups: {self.checker.counter}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'Mid Pushups: {self.checker.partial_counter}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(img, f'Feedback: {self.checker.feedback}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        return frame.from_ndarray(img, format="bgr24")
