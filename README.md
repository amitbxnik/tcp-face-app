# Face Recognition Application for UNIV 3000 Technical Competency Project

This is a Django-based web application that performs face recognition using the face_recognition Python library. The app allows users to interact with a simple web interface to upload images, which are then processed on the backend using a face detection algorithm.

---

## Structure

### `views.py`

Handles HTTP requests and routes within the Django application. The file:

- Receives uploaded image data from the frontend.
- Calls functions from `faceEngine.py` to perform face recognition.
- Returns results (e.g., annotated images or labels) to the frontend.

### `faceEngine.py`

This is the core logic engine for face detection/recognition. The file:

- Processes image data and returns information like:
  - Number of faces detected
  - Bounding boxes or facial landmarks

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
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. **Create a virtual environment & install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. **Run migrations & start the server**

```bash
python manage.py migrate
python manage.py runserver
```

4. Open your browser at `http://127.0.0.1:8000`

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

