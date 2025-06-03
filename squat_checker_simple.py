from is_functions import *
import time


# Define Squat States
class SquatState:
    NOT_SQUAT = "not_squat"
    FULL_UP = "full_up"
    MIDWAY = "midway"
    DOWN = "down"

class SquatChecker:
    def __init__(self, log_file=None):
        self.state = SquatState.NOT_SQUAT
        self.counter = 0
        self.partial_counter = 0
        self.feedback = "Get into Squat position"
        self.knee_lockout_angle = None
        self.up_state_start_time = None
        self.up_count = 0
        self.bottom_flag = False

    def update(self, landmarks, mp_pose):
        keypoints = get_main_body_points(landmarks, mp_pose)

        # Extract points
        l_shoulder = keypoints["left_shoulder"]
        l_wrist = keypoints["left_wrist"]
        l_hip = keypoints["left_hip"]
        l_knee = keypoints["left_knee"]
        l_ankle = keypoints["left_ankle"]

        r_shoulder = keypoints["right_shoulder"]
        r_wrist = keypoints["right_wrist"]
        r_hip = keypoints["right_hip"]
        r_knee = keypoints["right_knee"]
        r_ankle = keypoints["right_ankle"]

        if not is_shoulder_wrist_lvl(l_wrist, r_wrist, l_shoulder, r_shoulder):
            self.state = SquatState.NOT_SQUAT
            self.knee_lockout_angle = None
            self.feedback = "Get into Squat position"
            return

        if is_shoulder_wrist_lvl(l_wrist, r_wrist, l_shoulder, r_shoulder):
            if self.state == SquatState.NOT_SQUAT:
                if self.counter == 0:
                    if is_up_position_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                        self.state = SquatState.FULL_UP
                        self.up_state_start_time = time.time()
                        self.feedback = "Hold still 2s to calibrate..."
                    return
                if self.counter >= 0 or self.partial_counter >= 0:
                    if is_up_position_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                        self.state = SquatState.FULL_UP
                        #self.feedback = "Squat position detected, restart"

            if self.state == SquatState.FULL_UP:
                if self.knee_lockout_angle is None:
                    if time.time() - self.up_state_start_time >= 2.0:
                        if is_knees_visible(l_knee, r_knee):
                            l_angle = calculate_angle(l_hip, l_knee, l_ankle)
                            r_angle = calculate_angle(r_hip, r_knee, r_ankle)
                            self.knee_lockout_angle = max(l_angle, r_angle)
                            self.feedback = "Calibrated. Start squats!"

                if self.up_count == 1 and self.bottom_flag == True:
                    self.counter += 1
                    self.feedback = "Perfect Squat Done!"
                    self.up_count = 0
                    self.bottom_flag = False

                if self.up_count == 1 and self.bottom_flag == False:
                    self.partial_counter += 1
                    self.feedback = "Midway Squat Done!"
                    self.up_count = 0

                if self.partial_counter - 2 > self.counter:
                    self.feedback = "GET LOWER!"

                if is_mid_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                    self.feedback = "Midway Position Reached!"
                    self.state = SquatState.MIDWAY

            if self.state == SquatState.MIDWAY:

                l_angle = calculate_angle(l_hip, l_knee, l_ankle)
                r_angle = calculate_angle(r_hip, r_knee, r_ankle)
                current_angle = max(l_angle, r_angle)

                if current_angle > self.knee_lockout_angle - 3:
                    self.up_count += 1
                    self.feedback = "Up position Reached!"
                    self.state = SquatState.FULL_UP

                if is_down_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                    self.bottom_flag = True
                    self.feedback = "Down Position Reached!"
                    self.state = SquatState.DOWN


            if self.state == SquatState.DOWN:
                if is_mid_squat(l_knee,r_knee, l_ankle, r_ankle, l_hip, r_hip):
                    self.feedback = "Midway Position Reached!"
                    self.state = SquatState.MIDWAY