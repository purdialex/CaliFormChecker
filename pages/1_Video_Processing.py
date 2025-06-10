import streamlit as st
import tempfile
from modes.video_mode_pushup import video_pose_landmarks as pushup_processor
from modes.video_mode_pushup import video_pose_landmarks as squat_processor

st.title("Upload video for analysis")

mode = st.radio("Choose exercise type:", ["Pushup", "Squat"])

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi"])


if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_video_path = temp_input.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
        output_video_path = temp_output.name

    st.info("⏳ Processing your video... Please wait.")

    if mode == "Pushup":
        pushup_processor(input_video_path, output_video_path)
    if mode == "Squat":
        squat_processor(input_video_path, output_video_path)

    st.success("✅ Processing complete!")

    with open(output_video_path, 'rb') as file:
        st.video(file.read())
    with open(output_video_path, "rb") as file:
        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="video_processed.mp4",
            mime="video/mp4"
        )