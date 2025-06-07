import streamlit as st

st.set_page_config(page_title="Pushup Tutorial", layout="centered")

st.title("Pushup Tutorial")

st.markdown("""
Welcome to the pushup tutorial!  
Here you will learn how to do perfect pushups with examples.
""")

# Explanation text
st.write("""
- Keep your back straight  
- Lower yourself until your elbows are at 90 degrees  
- Push back up fully  
- Keep your core engaged  
""")

# Example video
tutorial_video_path = "D:\Coding chestii\PythonProject\pages\FullSizeRender2nd.mp4"
st.video(tutorial_video_path)
