import streamlit as st
from streamlit_webrtc import webrtc_streamer

from modes.streamlit_push_camera import PushupCameraProcessor
from modes.streamlit_squat_camera import SquatCameraProcessor

st.set_page_config(page_title="Webcam Mode", layout="centered")

# Inject CSS styling and animations
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

# Page heading with animation
st.markdown('<h1 class="fade-1">🎥 Webcam Mode</h1>', unsafe_allow_html=True)
st.markdown('<p class="fade-2">Turn on your webcam to receive live feedback on your exercise form.</p>', unsafe_allow_html=True)

# Info box animation
st.markdown("""
<div class="highlight-box fade-3">
    ⚠️ Ensure you're fully visible in the frame. Stand still for 2 seconds to allow elbow/knee calibration before starting!
</div>
""", unsafe_allow_html=True)

# Exercise mode selection
mode = st.radio("Choose exercise type:", ["Pushup", "Squat"])
if mode == "Pushup":
    processor = PushupCameraProcessor
if mode == "Squat":
    processor = SquatCameraProcessor

# Streamlit WebRTC camera processing
webrtc_streamer(
    key="live-processing",
    video_processor_factory=processor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
