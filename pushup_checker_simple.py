from utils import get_main_body_points, calculate_angle


# Define Pushup States (simplified)
class PushupState:
    UP = "up"
    DOWN = "down"

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

    avg_wrist_y = (left_wrist[1] + right_wrist[1]) / 2
    avg_ankle_y = (left_ankle[1] + right_ankle[1]) / 2

    #if shoulders and hips are nearly level

    #0.15, 0.15
    is_horizontal = abs(avg_shoulder_y - avg_hip_y) < 0.3

    is_wrist_ankle_lvl = (avg_wrist_y - avg_hip_y) < 0.6

    is_not_vertical = (avg_hip_y - avg_shoulder_y) < 0.3


    return (is_horizontal
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


class PushupChecker:
    def __init__(self):
        self.state = PushupState.UP
        self.counter = 0
        #self.feedback = "Start in plank position"

    def update(self, landmarks, mp_pose):
        keypoints = get_main_body_points(landmarks, mp_pose)

        # Extract keypoints
        left_wrist = keypoints["left_wrist"]
        left_elbow = keypoints["left_elbow"]
        left_shoulder = keypoints["left_shoulder"]
        left_hip = keypoints["left_hip"]
        left_knee = keypoints["left_knee"]
        left_ankle = keypoints["left_ankle"]

        right_wrist = keypoints["right_wrist"]
        right_elbow = keypoints["right_elbow"]
        right_shoulder = keypoints["right_shoulder"]
        right_hip = keypoints["right_hip"]
        right_knee = keypoints["right_knee"]
        right_ankle = keypoints["right_ankle"]

        if not is_body_plank(left_shoulder, left_hip, left_knee, left_ankle, left_wrist,
                             right_shoulder, right_hip, right_knee, right_ankle, right_wrist):
            self.feedback = "Get into proper plank position"
            return
        else:
            if self.counter == 0:
                self.feedback = "Body is in plank, start"
            if self.counter > 0:
                self.feedback = "Body is back in plank, continue"

        if self.state == PushupState.UP:
            if self.counter == 0:
                self.feedback = "Body is alligned, start"
            else:
                self.feedback = "Lower Down"
            if is_in_down_position(left_shoulder, left_elbow, left_wrist,
                                   right_shoulder, right_elbow, right_wrist):
                self.state = PushupState.DOWN
                #self.feedback = "Go down slowly" if self.counter == 0 else "Lower down"

        elif self.state == PushupState.DOWN:
            self.feedback = "Push Back Up"
            if is_in_up_position(left_shoulder, left_elbow, left_wrist,
                                 right_shoulder, right_elbow, right_wrist):
                self.state = PushupState.UP
                self.counter += 1
               # self.feedback = f"Pushup {self.counter} complete!"