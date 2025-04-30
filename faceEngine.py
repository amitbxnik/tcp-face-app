import cv2
import face_recognition
import os
import numpy as np

known_encodings = []
known_names = []

def scanKnownFaces(path="known_faces"): 
    # scans the faces that are in the known_faces directory and saves the names/encodings into an array for future ref.
    os.makedirs(path, exist_ok=True)
    for filename in os.listdir(path):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(path, filename)
            name = os.path.splitext(filename)[0] # get name from filename
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0]) # save the first encoding
                known_names.append(name) # save associated name
            else:
                print(f"There are no faces found in {filename}")

def imageFacialRecognition(image_path):
    #  performs facial recognition on an uploaded image & saves output image
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError("Error loading image. Please ensure the file is a valid image format.")
    # resize if too large
    max_width, max_height = 1280, 720
    height, width = frame.shape[:2]
    if width > max_width or height > max_height:
        scale_factor = min(max_width / width, max_height / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        frame = cv2.resize(frame, (new_width, new_height))

    frame = liveFacialRecognition(frame) # process image for facial recognition
    output_path = image_path.replace("uploads/", "uploads/processed_") # save processed image to a new path
    cv2.imwrite(output_path, frame)
    return output_path

def liveFacialRecognition(frame, scale=0.5):
   # detects & recognizes faces in a video frame, returning annotated frame.
    original_frame = frame.copy() #  keep OG frame if no faces are found
    small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale) # resize frame to speed up processing
    apply_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    model_to_use = "cnn" if cv2.cuda.getCudaEnabledDeviceCount() > 0 else "hog" # changes facial recognition engine based on device (improved performance)
    face_locations = face_recognition.face_locations(apply_rgb, model=model_to_use, number_of_times_to_upsample=1) # detect face location
    if len(face_locations) == 0: # if faces aren't found, retry with less upsampling
        face_locations = face_recognition.face_locations(apply_rgb, number_of_times_to_upsample=0)
    boxes = [] # array of bounding boxes
    names = [] # array of name labels
    if face_locations:
        face_encodings = face_recognition.face_encodings(apply_rgb, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            if known_encodings: # compares encoding w/ known faces in database
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                if len(distances) > 0:
                    best_match_index = np.argmin(distances)
                    if distances[best_match_index] < 0.5:
                        name = known_names[best_match_index] # recognized face

            # scales bounding box to OG frame size
            x1 = int(left / scale)
            y1 = int(top / scale)
            x2 = int(right / scale)
            y2 = int(bottom / scale)
            w = x2 - x1
            h = y2 - y1
            boxes.append([x1, y1, w, h])
            names.append(name)
        
       # helps with removing overlapping boxes
        if boxes:
            scores = [0.5] * len(boxes)
            indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.3, nms_threshold=0.4)
            if len(indices) > 0:
                indices = indices.flatten().tolist()
            else:
                indices = list(range(len(boxes)))
        else:
            indices = list(range(len(boxes)))
        
        # draw boxes and names on frame
        for i in indices:
            (x, y, w, h) = boxes[i]
            name = names[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            label_height = 15
            cv2.rectangle(frame, (x, y + h - label_height), (x + w, y + h), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (x + 5, y + h - 5), font, 0.5, (0, 0, 0), 1)
            
    else:
        # return OG frame if there are no faces detected.
        return original_frame 

    return frame