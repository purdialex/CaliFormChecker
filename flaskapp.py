from flask import Flask, request, send_file, render_template
import os
import uuid

# Import your video processing function
from modes.video_mode_pushup import *

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Add this route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return {"error": "No video file provided."}, 400

    video_file = request.files['video']
    if video_file.filename == '':
        return {"error": "No selected file."}, 400

    input_path = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()) + "_" + video_file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "processed_" + os.path.basename(input_path))

    video_file.save(input_path)

    # Use your mode function to process the video
    video_pose_landmarks(input_path, output_path)

    return send_file(output_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
