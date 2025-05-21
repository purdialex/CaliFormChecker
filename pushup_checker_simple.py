from utils import get_main_body_points, calculate_angle
from is_functions import *

# Define Pushup States (simplified)
class PushupState:
    MID_UP = "mid_up"
    UP = "up"
    DOWN = "down"




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
                #Body is calibrating, wait for one second then
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



            '''
            if self.state == PushupState.UP:
    if self.counter == 0:
        if self.up_state_start_time is None:
            # First time entering UP state — mark time
            self.up_state_start_time = time.time()
            self.feedback = "Hold still for calibration..."

        elif time.time() - self.up_state_start_time >= 1.0:
            # It's been 1 second — do the calibration
            l_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            r_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            self.initial_elbow_angles = (l_angle, r_angle)

            self.feedback = "Calibration complete. Begin pushups."
            self.state = PushupState.CHECK
            
            
            '''