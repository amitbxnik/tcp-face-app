# Face Recognition Application for UNIV 3000 Technical Competency Project

This is a web-based face recognition app built with Django on the backend and styled using HTML + Bootstrap on the frontend. It uses OpenCV and the face_recognition Python library to perform real-time facial detection and recognition on uploaded images or snapshots taken directly from the user's browser.

---

## Structure

```
TCP-face-app/
├── TCP_facial_recognition_project/
│   └── settings.py
│       # Django settings (env-based config, middleware, staticfiles, etc.)
│
├── detection_app/
│   └── views.py
│       # Django views handling uploads, snapshots, live-feed routing
│
├── faceEngine.py
│   # Core Python module for face detection & recognition logic
│
├── templates/
│   ├── index.html
│   │   # Homepage with browser-capture UI
│   ├── upload.html
│   │   # Traditional file-upload page
│   ├── add.html
│   │   # Form to register new “known” faces
│   ├── result.html
│   │   # Shows processed image results
│   └── success.html
│       # Confirmation after adding a face
│
├── known_faces/
│   # Directory of images used to build your face database
│
├── uploads/
│   # Temporarily holds user uploads & processed images
│
├── Deploy/
│   ├── Dockerfile
│   │   # Docker container setup for production
│   └── Procfile
│       # Process declaration for PaaS (Heroku, Railway, etc.)
│
├── old_approach/
│   └── app.py
│       # Legacy Flask-style demo (kept for reference)
│
├── requirements.txt
│   # List of Python packages (Django, OpenCV, face_recognition, etc.)
│
├── README.md
│   # Project overview, setup & deployment instructions
│
└── manage.py
    # Django’s command-line utility (runserver, migrations, etc.)
```

### Note: This is a simplified view. You can explore the full structure in your IDE or via terminal.

---

## Features

- Upload and process images via web UI
- Perform face detection or recognition
- Modular design with clean separation between views and detection engine
- Django backend with customizable routing

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/amitbxnik/tcp-face-app.git
cd tcp-face-app
```

2. **Create a .env from the example**

```bash
cp .env.example .env
# Then edit .env with your SECRET_KEY and hosts
```

3. **Create a virtual environment & install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

4. **Run migrations & start the server**

```bash
python manage.py migrate
python manage.py runserver
```

5. Open your browser at `http://127.0.0.1:8000`

---

## Deployment

This repo includes a Deploy/ folder with ready-to-use deployment configurations:

- Deploy/Dockerfile: Defines a Docker image with all system dependencies (OpenCV, dlib, ffmpeg, etc.) and collects static files.

- Deploy/Procfile: Specifies the command to run your app on platforms like Heroku or Railway.

To deploy using these configurations, follow your platform’s guide and point it at the Deploy/ folder. The old_approach/app.py contains a legacy Flask implementation for reference and is no longer actively maintained.

---

## Requirements

- Python 3.8+
- Django 3.x or 4.x
- OpenCV, Dlib, or other ML libraries (depending on `faceEngine.py`)

---

## Future Enhancements

- Add face labeling and recognition across users
- Store image metadata in a database
- Deploy application to a hosting website for demo

---
