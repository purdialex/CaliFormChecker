from is_functions import *
import csv
import time


# Define Pushup States
class PushupState:
    NOT_PLANK = "not_plank"
    FULL_UP = "full_up"
    MIDWAY_UP = "midway_up"
    DOWN = "down"


class PushupChecker:
    def __init__(self, log_file=None):
        self.state = PushupState.NOT_PLANK
        self.counter = 0
        self.partial_counter = 0
        self.feedback = "Get into plank position"
        self.elbow_lockout_angle = None
        self.up_state_start_time = None
        self.frame_index = 0

        self.log_file = log_file
        if self.log_file:
            self.init_csv()

    def init_csv(self):
        header = ["frame"]
        # 12 keypoints * 3 coords (x, y, z)
        for kp in ["left_shoulder", "left_elbow", "left_wrist", "left_hip", "left_knee", "left_ankle",
                   "right_shoulder", "right_elbow", "right_wrist", "right_hip", "right_knee", "right_ankle"]:
            header += [f"{kp}_x", f"{kp}_y", f"{kp}_z"]
        header.append("label")
        with open(self.log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    def log_frame(self, keypoints):
        row = [self.frame_index]
        for name in ["left_shoulder", "left_elbow", "left_wrist", "left_hip", "left_knee", "left_ankle",
                     "right_shoulder", "right_elbow", "right_wrist", "right_hip", "right_knee", "right_ankle"]:
            coords = keypoints[name]
            row += [coords[0], coords[1], coords[2]]
        row.append(self.state)
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        self.frame_index += 1


    def update(self, landmarks, mp_pose):
        keypoints = get_main_body_points(landmarks, mp_pose)

        # Extract points
        l_shoulder = keypoints["left_shoulder"]
        l_elbow = keypoints["left_elbow"]
        l_wrist = keypoints["left_wrist"]
        l_hip = keypoints["left_hip"]
        l_knee = keypoints["left_knee"]
        l_ankle = keypoints["left_ankle"]

        r_shoulder = keypoints["right_shoulder"]
        r_elbow = keypoints["right_elbow"]
        r_wrist = keypoints["right_wrist"]
        r_hip = keypoints["right_hip"]
        r_knee = keypoints["right_knee"]
        r_ankle = keypoints["right_ankle"]

        if not is_body_plank(l_shoulder, l_hip, l_knee, l_ankle, l_wrist,
                             r_shoulder, r_hip, r_knee, r_ankle, r_wrist):
            self.state = PushupState.NOT_PLANK
            self.elbow_lockout_angle = None
            self.feedback = "Get into Plank"
            return

        if is_body_plank(l_shoulder, l_hip, l_knee, l_ankle, l_wrist,
                         r_shoulder, r_hip, r_knee, r_ankle, r_wrist):
            if self.state == PushupState.NOT_PLANK:
                if self.counter == 0:
                    if is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
                        self.state = PushupState.FULL_UP
                        self.up_state_start_time = time.time()
                        self.feedback = "Hold still 2s to calibrate..."
                    return
                if self.counter >=0 or self.partial_counter >=0:
                    if is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
                        self.state = PushupState.FULL_UP
                        self.feedback = "Plank Detected, Restart"

            if self.state == PushupState.FULL_UP:
                if self.elbow_lockout_angle is None:
                    if time.time() - self.up_state_start_time >= 2.0:
                        # Calibrate lockout angle once
                        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
                        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                        self.elbow_lockout_angle = max(l_angle, r_angle)
                        self.feedback = "Calibrated. Start pushups!"
                else:
                    if is_in_down_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
                        self.state = PushupState.DOWN
                        self.feedback = "Pushup down position reached"

            if self.state == PushupState.DOWN:
                if is_in_up_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
                    self.state = PushupState.MIDWAY_UP

            if self.state == PushupState.MIDWAY_UP:
                l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
                r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                current_angle = max(l_angle, r_angle)
                if current_angle > self.elbow_lockout_angle - 3:
                    self.counter += 1
                    self.feedback = f"Full pushup! Total: {self.counter}"
                    self.state = PushupState.FULL_UP
                if is_in_down_position(l_shoulder, l_elbow, l_wrist, r_shoulder, r_elbow, r_wrist):
                    self.partial_counter += 1
                    self.feedback = f"Partial pushup! Total: {self.partial_counter}"
                    self.state = PushupState.DOWN

        if self.log_file:
            self.log_frame(keypoints)