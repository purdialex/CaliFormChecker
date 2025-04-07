import numpy as np
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def get_coords(landmarks, landmark_enum):
    lm = landmarks[landmark_enum.value]
    return [lm.x, lm.y]

def is_angle_within_range(angle, target, tolerance=10):
    return target - tolerance <= angle <= target + tolerance

def draw_landmarks_with_feedback(frame, results, feedback_text=None):
    mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
    )
    if feedback_text:
        cv2.putText(frame, feedback_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0) if "Good" in feedback_text else (0, 0, 255), 2)

def get_distance(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.linalg.norm(p1 - p2)
