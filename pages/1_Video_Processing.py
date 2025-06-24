import streamlit as st
import tempfile
from modes.video_mode_pushup import video_pose_landmarks as pushup_processor
from modes.video_mode_squat import video_pose_landmarks as squat_processor

st.set_page_config(page_title="Video Upload", layout="centered")

st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #FFA500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom animations and styles
st.markdown("""
    <style>
    html, body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
    }
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .fade-1, .fade-2, .fade-3 {
        opacity: 0;
        animation-name: fadeSlideUp;
        animation-fill-mode: forwards;
        animation-timing-function: ease-out;
    }
    .fade-1 { animation-delay: 0.2s; animation-duration: 0.8s; }
    .fade-2 { animation-delay: 0.5s; animation-duration: 0.8s; }
    .fade-3 { animation-delay: 0.8s; animation-duration: 0.8s; }
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

# UI Headings
st.markdown('<h1 class="fade-1">📹 Upload Video for Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="fade-2">Choose an exercise and upload your video to receive AI-powered feedback.</p>', unsafe_allow_html=True)
st.markdown('<p class = "fade-3">In order to upload more videos and download them without refreshing the order of operation is the following: Upload->Download->Press x On The Video Preview->Reset->Choose Exercise->Upload Again', unsafe_allow_html=True)
st.markdown("""
<div class="highlight-box fade-3">
    ⚠️ Make sure your full body is visible in the frame and allow 2 seconds for calibration at the start.
</div>
""", unsafe_allow_html=True)

# UI Controls
mode = st.radio("Choose exercise type:", ["Pushup", "Squat"])
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mpeg4"])

# Reset button
if st.button("🔁 Reset"):
    st.session_state.clear()
    st.rerun()

# Main logic
if uploaded_file is not None:
    # Check if uploaded file is new or different from last
    if ("processed_video_path" not in st.session_state or
        st.session_state.get("last_uploaded_file") != uploaded_file.name):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            temp_input.write(uploaded_file.read())
            input_video_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
            output_video_path = temp_output.name

        # Save to session state
        st.session_state["input_video_path"] = input_video_path
        st.session_state["processed_video_path"] = output_video_path
        st.session_state["last_uploaded_file"] = uploaded_file.name

        st.info("⏳ Processing your video... Please wait.")
        progress_bar = st.progress(0)
        status_text = st.empty()

        if mode == "Pushup":
            pushup_processor(input_video_path, output_video_path, progress_bar, status_text)
        else:
            squat_processor(input_video_path, output_video_path, progress_bar, status_text)

        st.success("✅ Processing complete!")
    else:
        st.success("✅ Using previously processed video!")

    # Display and download
    with open(st.session_state["processed_video_path"], 'rb') as file:
        st.video(file.read())
        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="video_processed.mp4",
            mime="video/mp4"
        )
