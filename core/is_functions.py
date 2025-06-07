from core.utils import get_main_body_points, calculate_angle


def is_shoulder_wrist_lvl(left_wrist, right_wrist, left_shoulder, right_shoulder):
    avg_wrist_y = (left_wrist[1] + right_wrist[1]) / 2
    avg_shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2

    is_hands_ok = abs(avg_wrist_y - avg_shoulder_y) < 0.2

    return is_hands_ok



def is_knees_visible(left_knee, right_knee):
    return 0 <= left_knee[1] <= 1 and 0 <= right_knee[1] <= 1

def is_mid_squat(left_knee, right_knee, left_ankle, right_ankle, left_hip, right_hip):
    l_angle = calculate_angle(left_hip, left_knee, left_ankle)
    r_angle = calculate_angle(right_hip, right_knee, right_ankle)

    return max(l_angle, r_angle) < 130

def is_down_squat(left_knee, right_knee, left_ankle, right_ankle, left_hip, right_hip):
    l_angle = calculate_angle(left_hip, left_knee, left_ankle)
    r_angle = calculate_angle(right_hip, right_knee, right_ankle)

    return  max(l_angle, r_angle) < 80

def is_up_position_squat(left_knee, right_knee, left_ankle, right_ankle, left_hip, right_hip):
    l_angle = calculate_angle(left_hip, left_knee, left_ankle)
    r_angle = calculate_angle(right_hip, right_knee, right_ankle)

    return max(l_angle, r_angle) > 170

def is_wrist_below_knees(left_wrist, right_wrist, left_knee, right_knee):

    avg_wrist_y = (left_wrist[1] + right_wrist[1]) / 2
    avg_knee_y = (left_knee[1] + right_knee[1]) / 2

    return avg_wrist_y > avg_knee_y


def is_knees_straight(left_hip, left_knee, left_ankle,
                      right_hip, right_knee, right_ankle):

    l_knee_angle = calculate_angle(left_hip,left_knee,left_ankle)
    r_knee_angle = calculate_angle(right_hip,right_knee,right_ankle)

    return l_knee_angle > 105 and r_knee_angle > 105

def is_body_plank(left_shoulder, left_hip, left_knee, left_ankle, left_wrist,
                  right_shoulder, right_hip, right_knee, right_ankle, right_wrist):

    avg_shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
    avg_hip_y = (left_hip[1] + right_hip[1]) / 2


    #0.15, 0.15
    is_horizontal = abs(avg_shoulder_y - avg_hip_y) < 0.3


    is_not_vertical = (avg_hip_y - avg_shoulder_y) < 0.3


    return     (is_horizontal
            and is_not_vertical
            and is_wrist_below_knees(left_wrist, right_wrist, left_knee, right_knee)
            and is_knees_straight(left_hip, left_knee, left_ankle, right_hip, right_knee, right_ankle))


def is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    return max(l_angle, r_angle) >= 142


def is_in_down_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    return max(l_angle, r_angle) < 125