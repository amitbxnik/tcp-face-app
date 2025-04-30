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

## Requirements

- Python 3.8+
- Django 3.x or 4.x
- OpenCV, Dlib, or other ML libraries (depending on `faceEngine.py`)

---
