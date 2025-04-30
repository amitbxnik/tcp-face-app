# INITIAL FLASK APPROACH, HAD TO SCRAP & REPLACE W/ DJANGO TO BETTER HANDLE VIDEO FEED
from flask import Flask, render_template, Response, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import atexit
from faceEngine import imageFacialRecognition, liveFacialRecognition, scanKnownFaces
import gc

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 # 5MB file limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
scanKnownFaces()
camera = None

def getCamera():
    global camera
    if camera is None or not camera.IsOpened():
        camera = cv2.VideoCapture(0)
    return camera

def releaseCamera():
    global camera
    if camera and camera.isOpened():
        camera.released()
        camera = None

atexit.register(releaseCamera)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def videoFeed():
    def generate_frames():
        cam = getCamera()
        try:
            while True:
                success, frame = cam.read()
                if not success:
                    break
                else:
                    processed_frame = liveFacialRecognition(frame, scale=1.0)
                    ret, buffer = cv2.imencode('.jpg', processed_frame)
                    frame_bytes = buffer.tobytes()
                    gc.collect()
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except GeneratorExit:
            pass
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/upload", methods=["GET", "POST"])
def uploadImage():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file part in request"

        file = request.files["image"]
        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            processed_path = imageFacialRecognition(path)
            processed_filename = os.path.basename(processed_path)
            return redirect(url_for('result', filename=processed_filename))
    return render_template('upload.html')

@app.route("/uploads/<filename>")
def uploadedFile(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/result/<filename>')
def result(filename):
    return render_template("result.html", filename=filename)

@app.teardown_appcontext
def cleanup(exception=None):
    gc.collect

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        releaseCamera()