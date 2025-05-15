from utils import get_main_body_points, calculate_angle

# Define Pushup States
class PushupState:
    UP = "up"
    DOWN = "down"
    CHECK = "check"

def is_body_horizontal(left_shoulder, left_hip, left_knee, right_shoulder, right_hip, right_knee):
    '''
    # Calculate torso angles
    left_torso_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    right_torso_angle = calculate_angle(right_shoulder, right_hip, right_knee)

    # Body is aligned if both angles are close to 180°
    #return abs(left_torso_angle - 150) < 15 and abs(right_torso_angle - 150) < 15
    max_angle = max(left_torso_angle, right_torso_angle)
    return max_angle > 140
    '''
    #We used the y coordinates to calculate if its vertical or horizontal
    avg_shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
    avg_hip_y = (left_hip[1] + right_hip[1]) / 2

    # Vertical threshold - if shoulders and hips are nearly at same height (plank)
    is_horizontal = abs(avg_shoulder_y - avg_hip_y) < 0.15  #how strict plank is

    # Additional check to prevent vertical position (standing)
    # In standing position, hips would be much lower than shoulders
    is_not_vertical = (avg_hip_y - avg_shoulder_y) < 0.4  #how much hip drop before its just standing vertical

    return is_horizontal and is_not_vertical


def is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    max_angle = max(l_angle, r_angle)  # Take the more extended arm
    return max_angle >= 142


def is_in_down_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
    l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
    r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
    min_angle = min(l_angle, r_angle)  # Take the more bent arm
    return min_angle < 95


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

        right_wrist = keypoints["right_wrist"]
        right_elbow = keypoints["right_elbow"]
        right_shoulder = keypoints["right_shoulder"]
        right_hip = keypoints["right_hip"]
        right_knee = keypoints["right_knee"]

        # Check for body alignment first
        if is_body_horizontal(left_shoulder, left_hip, left_knee, right_shoulder, right_hip, right_knee):
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
                        self.feedback = "Push Up Position is correct"

                if is_in_down_position(left_shoulder, left_elbow, left_wrist,
                                        right_shoulder, right_elbow, right_wrist):
                    self.feedback = "Push back up."
                    self.state = PushupState.DOWN

            elif self.state == PushupState.DOWN:
                if is_in_up_position(left_shoulder, left_elbow, left_wrist,
                                     right_shoulder, right_elbow, right_wrist):
                    self.feedback = "Good Pushup"
                    self.state = PushupState.UP  # Change state back to UP after a pushup
                    self.counter += 1  # Increment the pushup count
        else:
            self.feedback = "Get into the proper Pushup position"