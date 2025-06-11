import streamlit as st

st.set_page_config(page_title="Tutorial", layout="centered")

# Custom CSS with animations
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

# Animated title and description
st.markdown('<h1 class="fade-1">📖 Tutorial</h1>', unsafe_allow_html=True)
st.markdown('<p class="fade-2">Here you will learn how to perform key exercises correctly with examples.</p>', unsafe_allow_html=True)

# Animated warning box
st.markdown("""
<div class="highlight-box fade-3">
    ⚠️ Please wait 2 seconds for the system to calibrate your elbow or knee angle before starting the exercise.
</div>
""", unsafe_allow_html=True)

# Pushup Tutorial
st.header("Pushup Tutorial")
st.markdown("""
<ul>
  <li>Keep your back straight</li>
  <li>Lower yourself until your elbows are at 90 degrees</li>
  <li>Push back up fully</li>
  <li>Keep your core engaged</li>
</ul>
""", unsafe_allow_html=True)

# Pushup video
pushup_video_path = r"D:\Coding chestii\PythonProject\pages\FullSizeRender2nd.mp4"
st.video(pushup_video_path)

# Divider
st.markdown("<hr>", unsafe_allow_html=True)

# Squat Tutorial
st.header("Squat Tutorial")
st.markdown("""
<ul>
  <li>Stand with feet shoulder-width apart</li>
  <li>Keep your chest up and back straight</li>
  <li>Lower down as if sitting on a chair until your thighs are parallel to the floor</li>
  <li>Push through your heels to stand back up</li>
  <li>Engage your core throughout</li>
</ul>
""", unsafe_allow_html=True)

# Squat video
squat_video_path = r"D:\Coding chestii\PythonProject\pages\FullSizeRender2nd.mp4"
st.video(squat_video_path)
