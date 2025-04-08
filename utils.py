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
        "left_ankle": get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE),
        "right_shoulder": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER),
        "right_elbow": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW),
        "right_wrist": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST),
        "right_hip": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_HIP),
        "right_ankle": get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE),
    }
    return keypoints
def is_point_in_frame(point):
    x,y, _ = point
    if 0 <= x <= 1 and 0 <= y <= 1:
        return True
    return False
