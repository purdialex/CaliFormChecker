import cv2
import mediapipe as mp
from core.squat_checker_complex import SquatChecker
from core.utils import get_main_body_points, calculate_angle

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def video_pose_landmarks(input_video_path, output_video_path, progress_bar=None, status_text=None):
    if progress_bar is None:
        progress_bar = lambda x: None
    if status_text is None:
        status_text = lambda x: None

    checker = SquatChecker()
    cap = cv2.VideoCapture(input_video_path)
    rotation_code = None

    try:
        # Check for rotation metadata (some phones)
        rotation = int(cap.get(cv2.CAP_PROP_ORIENTATION_META))
        if rotation == 180:
            rotation_code = cv2.ROTATE_180
        elif rotation == 90:
            rotation_code = cv2.ROTATE_90_CLOCKWISE
        elif rotation == 270:
            rotation_code = cv2.ROTATE_90_COUNTERCLOCKWISE
    except:
        pass

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Resize dimensions: downscale to 1280x720 if larger
    target_width, target_height = frame_width, frame_height
    if frame_width > 1280 or frame_height > 720:
        aspect_ratio = frame_width / frame_height
        if aspect_ratio >= 16 / 9:
            target_width = 1280
            target_height = int(1280 / aspect_ratio)
        else:
            target_height = 720
            target_width = int(720 * aspect_ratio)

    target_size = (target_width, target_height)

    # Use 'mp4v' codec for wider compatibility
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, target_size)
    current_frame = 0

    with mp_pose.Pose(
        model_complexity=1,
        static_image_mode=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            current_frame += 1
            progress_ratio = current_frame / total_frames
            progress_bar.progress(min(progress_ratio, 1.0))
            status_text.text(f"Processing frame {current_frame}/{total_frames}...")

            if rotation_code is not None:
                frame = cv2.rotate(frame, rotation_code)


            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                checker.update(results.pose_landmarks, mp_pose)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Text overlays
                cv2.putText(frame, f'Good Squats: {checker.counter}', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Feedback: {checker.feedback}', (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0) if checker.feedback == "GET LOWER!" else (0, 255, 255), 2)
                cv2.putText(frame, f'Mid Squats: {checker.partial_counter}', (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Keypoint calculations
                keypoints = get_main_body_points(results.pose_landmarks, mp_pose)
                h, w, _ = frame.shape

                def draw_angle(name, color):
                    pt1 = keypoints[name[0]]
                    pt2 = keypoints[name[1]]
                    pt3 = keypoints[name[2]]
                    angle = int(calculate_angle(pt1, pt2, pt3))
                    px = int(pt2[0] * w), int(pt2[1] * h)
                    cv2.putText(frame, f'{angle}', (px[0], px[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 1)

                draw_angle(("left_shoulder", "left_elbow", "left_wrist"), (255, 0, 0))
                draw_angle(("right_shoulder", "right_elbow", "right_wrist"), (255, 0, 0))
                draw_angle(("left_hip", "left_knee", "left_ankle"), (0, 0, 255))
                draw_angle(("right_hip", "right_knee", "right_ankle"), (0, 0, 255))
                draw_angle(("left_shoulder", "left_hip", "left_knee"), (0, 255, 255))
                draw_angle(("right_shoulder", "right_hip", "right_knee"), (0, 255, 255))

            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        status_text.text("🎉 Processing complete!")
        progress_bar.progress(1.0)

# Uncomment if running as script
"""
input_path = input("Enter input video path: ")
output_path = input("Enter output video path (e.g., output.mp4): ")
video_pose_landmarks(input_path, output_path)
"""
