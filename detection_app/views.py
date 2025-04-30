import os
import cv2
import face_recognition
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from threading import Thread
from queue import Queue
import time

from faceEngine import imageFacialRecognition, liveFacialRecognition, scanKnownFaces

scanKnownFaces()

camera = None
frame_queue = Queue(maxsize=2) # holds a maximum of 2 frames for processing
processed_frame = None
processing_active = True

def get_camera(): # initializes camera (required for memory management)
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0) # opens camera if isn't previously open
        #lowers resolution for mem & easier processing
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera

def release_camera(): # releases camera from mem if in use (helps with previous crashing issues)
    global camera
    if camera and camera.isOpened():
        camera.release()
        camera = None

def process_frames():
    global processed_frame, processing_active
    while processing_active:
        if not frame_queue.empty():
            frame = frame_queue.get() # gets frame from queue & processes frame w/ facial recognition function
            processed = liveFacialRecognition(frame, scale=0.5)
            processed_frame = processed # stores processed frame for display
            frame_queue.task_done() # mark task as done
        else:
            time.sleep(0.01) # delay for CPU

# thread processing to address previously laggy camera 
processing_thread = Thread(target=process_frames, daemon=True) 
processing_thread.start()

def index(request):
    # renders homepage
    return render(request, "detection_app/index.html")

def gen_frames():
    global processed_frame
    cam = get_camera()
    last_frame = None
    
    try:
        while True:
            success, frame = cam.read() # attempt to read frame from camera
            if not success:
                break
            
            if not frame_queue.full(): # add copy of frame to queue if it's not full
                frame_queue.put(frame.copy())
            
            # show processed frame if available, otherwise show the raw frame
            display_frame = processed_frame if processed_frame is not None else frame
            last_frame = display_frame.copy()
            
            #encode frame as jpg file
            ret, buffer = cv2.imencode(".jpg", display_frame)
            frame_bytes = buffer.tobytes()
            
            # yield bytes in streaming format
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print(f"Stream error: {e}")

def video_feed(request):
    # streams the processed video to the frontend
    return StreamingHttpResponse(gen_frames(), 
                                content_type="multipart/x-mixed-replace; boundary=frame")

def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]

        VALID_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
        ext = os.path.splitext(image_file.name)[1].lower()
        if ext not in VALID_IMAGE_EXTENSIONS:
            return HttpResponse("Error: Invalid file type. Please upload an image.")
        
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file) # saves uploaded image
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)
        try: # attemps to process image & get result file path
            processed_path = imageFacialRecognition(uploaded_file_path)
            processed_filename = os.path.basename(processed_path)
            return redirect(reverse("result", kwargs={"filename": processed_filename}))
        except Exception as e:
            return HttpResponse(f"Error processing image: {e}")
    
    return render(request, "detection_app/upload.html")

def add_known_face(request):
    # method for users to add any faces of their choosing to database
    if request.method == "POST" and request.FILES.get("face_image"):
        face_image = request.FILES["face_image"]
        person_name = request.POST.get("person_name", "").strip()

        if not person_name:
            return HttpResponse("Error: Person name is required")
        
        filename = f"{person_name.replace(' ', '_')}.jpg"
        known_faces_dir = os.path.join(settings.BASE_DIR, "known_faces")
        os.makedirs(known_faces_dir, exist_ok=True)
        filepath = os.path.join(known_faces_dir, filename)
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        counter = 1

        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{ext}"
            filepath = os.path.join(known_faces_dir, filename)
            counter += 1

        with open(filepath, 'wb+') as destination:
            for chunk in face_image.chunks():
                destination.write(chunk)

        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            # If there isn't a face detected in the photo, throw error
            os.remove(filepath)
            return HttpResponse("Error: No face detected in the uploaded image")
        
        from faceEngine import known_encodings, known_names
        known_encodings.append(encodings[0])
        known_names.append(os.path.splitext(filename)[0])
        
        return redirect(reverse('face_added_success', kwargs={
            'filename': filename,
            'person_name': person_name.replace(' ', '_')
        }))
    
    return render(request, "detection_app/add.html")

def face_added_success(request, filename, person_name):
    display_name = person_name.replace(' ', ' ')
    context = {
        'filename': filename,
        'person_name': display_name,
        'redirect_url': reverse('index'),
        'redirect_delay': 5
    }
    return render(request, "detection_app/success.html", context)

def result(request, filename):
    # renders result page showing processed image
    return render(request, "detection_app/result.html", {"filename": filename})

import atexit
def cleanup():
    global processing_active
    processing_active = False
    release_camera() # release camera

atexit.register(cleanup) # call cleanup when program exits