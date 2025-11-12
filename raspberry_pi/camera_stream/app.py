from flask import Flask, render_template
from flask_socketio import SocketIO
from picamera2 import Picamera2
import cv2, base64, time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Pi Camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        encoded = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('video_frame', encoded)
        time.sleep(0.05)  # around 20 FPS

@socketio.on('connect')
def handle_connect():
    print("✅ Client connected")

if __name__ == "__main__":
    socketio.start_background_task(generate_frames)
    socketio.run(app, host="0.0.0.0", port=5000)
