import streamlit as st
import tempfile
from modes.video_mode_pushup import video_pose_landmarks

st.set_page_config(page_title="Pushup Analyzer", layout="centered")

st.title("🏋️‍♂️ Pushup Analyzer")
st.markdown("Upload a video and let AI analyze your pushups.")

st.markdown("""
Want to learn how to do a perfect pushup?  
Go to the **Tutorial** page from the sidebar!
""")

# File uploader
uploaded_file = st.file_uploader("Upload a pushup video", type=["mp4", "avi"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_video_path = temp_input.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
        output_video_path = temp_output.name

    st.info("⏳ Processing your video... Please wait.")
    video_pose_landmarks(input_video_path, output_video_path)
    st.success("✅ Processing complete!")

    with open(output_video_path, 'rb') as file:
        st.video(file.read())

    with open(output_video_path, "rb") as file:
        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="pushup_processed.mp4",
            mime="video/mp4"
        )
