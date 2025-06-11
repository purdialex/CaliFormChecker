from core.is_functions import *
import time


class SquatState:
    NOT_SQUAT = "not_squat"
    FULL_UP = "full_up"
    MIDWAY = "midway"
    DOWN = "down"


class SquatChecker:
    def __init__(self):
        self.state = SquatState.NOT_SQUAT
        self.prev_state = None

        self.counter = 0
        self.partial_counter = 0

        self.feedback = "Get into Squat position"
        self.feedback_timestamp = time.time()

        self.knee_lockout_angle = None
        self.up_state_start_time = None
        self.down_state_time = None

        self.up_count = 0
        self.bottom_flag = False

    def set_feedback(self, message):
        self.feedback = message
        self.feedback_timestamp = time.time()

    def update(self, landmarks, mp_pose):
        keypoints = get_main_body_points(landmarks, mp_pose)

        l_hip, l_knee, l_ankle = keypoints["left_hip"], keypoints["left_knee"], keypoints["left_ankle"]
        r_hip, r_knee, r_ankle = keypoints["right_hip"], keypoints["right_knee"], keypoints["right_ankle"]
        l_wrist, r_wrist = keypoints["left_wrist"], keypoints["right_wrist"]
        l_shoulder, r_shoulder = keypoints["left_shoulder"], keypoints["right_shoulder"]

        if not is_shoulder_wrist_lvl(l_wrist, r_wrist, l_shoulder, r_shoulder):
            self.state = SquatState.NOT_SQUAT
            self.knee_lockout_angle = None
            self.set_feedback("Get into Squat position")
            return

        # STATE: NOT_SQUAT
        if self.state == SquatState.NOT_SQUAT:
            if is_up_position_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                self.state = SquatState.FULL_UP
                self.up_state_start_time = time.time()
                self.set_feedback("Hold still 2s to calibrate...")
                return

        # STATE: FULL_UP
        if self.state == SquatState.FULL_UP:
            if self.knee_lockout_angle is None:
                if time.time() - self.up_state_start_time >= 2.0:
                    if is_knees_visible(l_knee, r_knee):
                        l_angle = calculate_angle(l_hip, l_knee, l_ankle)
                        r_angle = calculate_angle(r_hip, r_knee, r_ankle)
                        self.knee_lockout_angle = max(l_angle, r_angle)
                        self.set_feedback("Calibrated. Start squats!")
                        return

            if is_mid_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                self.state = SquatState.MIDWAY
                self.set_feedback("Midway Position Reached!")
                return

        # STATE: MIDWAY
        if self.state == SquatState.MIDWAY:
            if is_down_squat(l_knee, r_knee, l_ankle, r_ankle, l_hip, r_hip):
                self.state = SquatState.DOWN
                self.bottom_flag = True
                self.down_state_time = time.time()
                self.set_feedback("Down Position Reached!")
                return

            current_angle = max(
                calculate_angle(l_hip, l_knee, l_ankle),
                calculate_angle(r_hip, r_knee, r_ankle)
            )
            if self.knee_lockout_angle and current_angle > self.knee_lockout_angle - 10:
                self.partial_counter += 1
                if self.partial_counter - self.counter > 2 and self.bottom_flag == False:
                    self.set_feedback("GET LOWER!")
                else:
                    self.set_feedback("Partial Squat!")
                self.state = SquatState.FULL_UP
                return

        # STATE: DOWN
        if self.state == SquatState.DOWN:
            if time.time() - self.down_state_time < 0.2:
                return  # dwell time to stay in down position

            current_angle = max(
                calculate_angle(l_hip, l_knee, l_ankle),
                calculate_angle(r_hip, r_knee, r_ankle)
            )
            if self.knee_lockout_angle and current_angle > self.knee_lockout_angle - 10:
                self.counter += 1
                self.set_feedback("Full Squats!")
                self.bottom_flag = False
                self.state = SquatState.FULL_UP
                return
