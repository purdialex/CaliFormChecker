import cv2
import numpy as np

def get_coords(landmarks, landmark_enum):
    #Retrieves (x, y, z) coordinates for a specific landmark from the landmarks list.
    lm = landmarks.landmark[landmark_enum.value]
    return (lm.x, lm.y, lm.z)


def get_main_body_points(landmarks, mp_pose):
    #Returns a dictionary of key body landmarks and their (x, y, z) coordinates.
    keypoints = {
        "left_shoulder": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER),
        "left_elbow": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW),
        "left_wrist": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST),
        "left_hip": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_HIP),
        "left_knee": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_KNEE),
        "left_ankle": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE),

        "right_shoulder": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER),
        "right_elbow": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW),
        "right_wrist": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST),
        "right_hip": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_HIP),
        "right_knee": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE),
        "right_ankle": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE),
    }
    return keypoints
def is_point_in_frame(point):
    x,y, _ = point
    if 0 <= x <= 1 and 0 <= y <= 1:
        return True
    return False

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)


def draw_angle(img, name, pt1, pt2, pt3, color, h, w):
    """
    Draws the angle between three points on the image.

    Parameters:
    - img: The image to draw on
    - name: Name of the angle (not used now, but helpful for debugging or labeling)
    - pt1, pt2, pt3: The three keypoints
    - color: Color of the angle text
    - h, w: Height and width of the image
    """
    angle = calculate_angle(pt1, pt2, pt3)
    px = int(pt2[0] * w), int(pt2[1] * h)
    cv2.putText(img, f'{int(angle)}', (px[0], px[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)