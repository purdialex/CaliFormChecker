import streamlit as st

st.set_page_config(page_title="CaliFormChecker", layout="centered")

st.markdown("""
    <style>
    /* Apply global font family */
    html, body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
    }

    /* Animation keyframes */
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

    .title, .subtitle, .description, .button-container, .info-box {
        opacity: 0;
        animation-fill-mode: forwards;
        animation-timing-function: ease-out;
    }

    .title {
        animation-name: fadeSlideUp;
        animation-duration: 0.8s;
        animation-delay: 0.2s;
    }

    .subtitle {
        animation-name: fadeSlideUp;
        animation-duration: 0.8s;
        animation-delay: 0.5s;
    }

    .description {
        animation-name: fadeSlideUp;
        animation-duration: 0.8s;
        animation-delay: 0.8s;
    }

    .button-container {
        animation-name: fadeSlideUp;
        animation-duration: 0.8s;
        animation-delay: 1.1s;
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    .info-box {
        animation-name: fadeSlideUp;
        animation-duration: 0.8s;
        animation-delay: 1.4s;
        max-width: 600px;
        margin: 40px auto 30px auto;
        padding: 20px 25px;
        background: #fff4e6;
        border-radius: 15px;
        border: 2px solid #ff5900;
        color: #333;
        font-size: 1.1em;
        box-shadow: 0 6px 15px rgba(255, 89, 0, 0.15);
        text-align: center;
        font-style: italic;
    }

    .nav-card {
        background-color: white;
        border: 3px solid black;
        border-radius: 20px;
        width: 200px;
        text-align: center;
        padding: 30px 20px;
        text-decoration: none;
        color: black !important;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .nav-card:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #fff4e6, #ff5900);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }

    .nav-icon {
        font-size: 4em;
        margin-bottom: 15px;
        display: block;
        text-decoration: none !important;
    }

    a {
        text-decoration: none !important;
    }
    
    
    </style>

    <h1 class="title">🏋️ Cali Form Checker</h1>
    <p class="subtitle">Smart Pose-Based Workout Analysis for pushups, squats and pullups</p>
    <p class="description">
        Welcome to your AI-powered fitness companion. 
        Upload your workout videos or use your webcam to receive real-time feedback powered by computer vision.
        Please make sure to consult the tutorial before attempting the exercises!
    </p>

    <div class="button-container">
        <a href="/Video_Processing" class="nav-card">
            <span class="nav-icon">📹</span>
            <span>Upload Mode</span>
        </a>
        <a href="/Camera_Processing" class="nav-card">
            <span class="nav-icon">🎥</span>
            <span>Webcam Mode</span>
        </a>
        <a href="/Tutorial" class="nav-card">
            <span class="nav-icon">📖</span>
            <span>Tutorial</span>
        </a>
    </div>

    <div class="info-box">
        This project was created to simplify tracking and analyzing the main calisthenics exercises such as pushups, pull-ups, and squats. By leveraging AI and computer vision, it offers an easy-to-use fitness companion that helps users improve their form, monitor progress, and stay motivated on their workout journey. Whether you prefer uploading workout videos or using your webcam for real-time feedback, AI Fitness Coach aims to empower your fitness goals with smart, accessible technology.
    </div>
        
""", unsafe_allow_html=True)
