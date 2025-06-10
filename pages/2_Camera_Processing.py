import streamlit as st
from streamlit_webrtc import webrtc_streamer
from modes.streamlit_push_camera import PushupCameraProcessor
from modes.streamlit_squat_camera import SquatCameraProcessor

st.title("Turn on webcam for analysis")
mode = st.radio("Choose exercise type:", ["Pushup", "Squat"])
if mode == "Pushup":
    processor = PushupCameraProcessor
if mode == "Squat":
    processor = SquatCameraProcessor

webrtc_streamer(
    key="live-processing",
    video_processor_factory=processor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
