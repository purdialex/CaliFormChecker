import streamlit as st
import tempfile
from modes.video_mode_pushup import video_pose_landmarks as pushup_processor
from modes.video_mode_pushup import video_pose_landmarks as squat_processor

st.set_page_config(page_title="Video Upload", layout="centered")

# Inject custom style with animations
st.markdown("""
    <style>
    html, body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
    }

    @keyframes fadeSlideUp {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-1, .fade-2, .fade-3 {
        opacity: 0;
        animation-name: fadeSlideUp;
        animation-fill-mode: forwards;
        animation-timing-function: ease-out;
    }

    .fade-1 {
        animation-delay: 0.2s;
        animation-duration: 0.8s;
    }

    .fade-2 {
        animation-delay: 0.5s;
        animation-duration: 0.8s;
    }

    .fade-3 {
        animation-delay: 0.8s;
        animation-duration: 0.8s;
    }

    .highlight-box {
        background-color: #fff4e6;
        border: 2px solid #ff5900;
        border-radius: 12px;
        padding: 20px;
        font-size: 1.1em;
        color: #333;
        font-weight: 600;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 6px 15px rgba(255, 89, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Animated title
st.markdown('<h1 class="fade-1">📹 Upload Video for Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="fade-2">Choose an exercise and upload your video to receive AI-powered feedback.</p>', unsafe_allow_html=True)

# Animated info box
st.markdown("""
<div class="highlight-box fade-3">
    ⚠️ Make sure your full body is visible in the frame and allow 2 seconds for calibration at the start.
</div>
""", unsafe_allow_html=True)

# UI controls
mode = st.radio("Choose exercise type:", ["Pushup", "Squat"])
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi"])

# Processing logic
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
