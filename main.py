from modes.video_mode_pushup import *

input_path = "D:\Coding chestii\LandMarkFolder\InputVideo\FullSizeRender2nd.mp4"
output_path = "D:\Coding chestii\LandMarkFolder\OutputVideoNew\FullSizeRender2nd.mp4"


print(f"Processing {input_path} and saving to {output_path}...")
video_pose_landmarks(input_path, output_path)
print("Processing complete!")