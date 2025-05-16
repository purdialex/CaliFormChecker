from utils import get_main_body_points, calculate_angle

# Define Pushup States
class PushupState:
    UP = "up"
    DOWN = "down"
    CHECK = "check"

def is_body_plank(left_shoulder, left_hip  , left_knee, left_ankle, right_shoulder, right_hip, right_knee, right_ankle):
    #We used the y coordinates to calculate if its vertical or horizontal
    avg_shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
    avg_hip_y = (left_hip[1] + right_hip[1]) / 2

    # Vertical threshold - if shoulders and hips are nearly at same height (plank)
    ################################################it was 0.15 before
    is_horizontal = abs(avg_shoulder_y - avg_hip_y) < 0.15  #how strict plank is

    # Additional check to prevent vertical position (standing)
    # In standing position, hips would be much lower than shoulders
    is_not_vertical = (avg_hip_y - avg_shoulder_y) < 0.4  #how much hip drop before its just standing vertical


    #l_angle = calculate_angle(left_hip, left_knee, left_ankle)
    #r_angle = calculate_angle(right_hip, right_knee, right_ankle)
    # min_angle = min(l_angle, r_angle)

    return is_horizontal and is_not_vertical # and min_angle > 125



def is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    max_angle = max(l_angle, r_angle)  # Take the more extended arm
    return max_angle >= 142


def is_in_down_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    min_angle = min(l_angle, r_angle)  # Take the more bent arm
    #trying with max_angle
    max_angle = max(l_angle, r_angle)
    #return min_angle < 95
    return max_angle < 125

class PushupChecker:
    def __init__(self):
        self.state = PushupState.UP  # Initial state is UP
        self.counter = 0
        self.feedback = "Start in Pushup Position"

    def update(self, landmarks, mp_pose):

        keypoints = get_main_body_points(landmarks, mp_pose)

        # Extract keypoints for arms and torso
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

        # Check for body alignment first
        #if is_body_horizontal(left_shoulder, left_hip, left_knee, right_shoulder, right_hip, right_knee):
        if is_body_plank(left_shoulder, left_hip  , left_knee, left_ankle, right_shoulder, right_hip, right_knee, right_ankle):
            if self.state == PushupState.UP:
                if is_in_up_position(left_shoulder, left_elbow, left_wrist,
                                      right_shoulder, right_elbow, right_wrist):
                    if self.counter == 0:
                        self.feedback = "Push Up Position is correct"
                        self.state = PushupState.CHECK
                    else:
                        self.feedback = "Lower down for next pushup."
                        self.state = PushupState.CHECK

            elif self.state == PushupState.CHECK:
                if is_in_up_position(left_shoulder, left_elbow, left_wrist,
                                     right_shoulder, right_elbow, right_wrist):
                    if self.counter == 0:
                        self.feedback = "Push Up Position is correct, start"

                if is_in_down_position(left_shoulder, left_elbow, left_wrist,
                                        right_shoulder, right_elbow, right_wrist):
                    self.feedback = "Push back up."
                    self.state = PushupState.DOWN

            elif self.state == PushupState.DOWN:
                if is_in_up_position(left_shoulder, left_elbow, left_wrist,
                                     right_shoulder, right_elbow, right_wrist):
                    self.feedback = "Pushup DONE"
                    self.state = PushupState.UP  # Change state back to UP after a pushup
                    self.counter += 1  # Increment the pushup count
        else:
            self.feedback = "Get into the proper Pushup position"