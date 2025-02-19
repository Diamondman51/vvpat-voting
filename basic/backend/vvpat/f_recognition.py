import os
import sys
import django
import cv2
import face_recognition

# Setup Django environment
sys.path.append(r'E:/vvpat-voting/basic/backend')  # Add your Django project directory to the Python path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")  # Use the correct settings module
django.setup()

from vvpat.models import Voter

def load_known_faces():
    """Load known faces from the database and encode them."""
    print("Loading known faces from the database...")
    voters = Voter.objects.all()
    known_face_encodings = []
    known_face_names = []

    for voter in voters:
        try:
            known_image = face_recognition.load_image_file(voter.image.path)
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(known_encoding)
            known_face_names.append([voter.user_id.first_name, voter])
        except Exception as e:
            print(f"Error processing image for {voter.user_id.first_name}: {e}")

    return known_face_encodings, known_face_names

def process_frame(frame, known_face_encodings, known_face_names):
    """Process a single frame for face recognition."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index][0]
            voter: Voter = known_face_names[match_index][1]
            voter.refresh_from_db()
            voter.is_registered = True
            voter.save()

        face_names.append(name)

    return face_locations, face_names

def draw_face_annotations(frame, face_locations, face_names):
    """Draw rectangles and labels around detected faces."""
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (255, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

def main():
    cv2.ocl.setUseOpenCL(True)
    known_face_encodings, known_face_names = load_known_faces()

    video_capture = cv2.VideoCapture(0)  # 0 for the default webcam
    if not video_capture.isOpened():
        print("Error: Could not open video capture.")
        return

    print("Starting real-time face recognition... Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        face_locations, face_names = process_frame(frame, known_face_encodings, known_face_names)
        draw_face_annotations(frame, face_locations, face_names)

        cv2.imshow("Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()






# import os
# import sys
# import django
# import cv2
# import face_recognition
# cv2.ocl.setUseOpenCL(True)

# # Setup Django environment
# sys.path.append(r'E:/vvpat-voting/basic/backend')  # Add your Django project directory to the Python path
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")  # Use the correct settings module
# django.setup()

# from vvpat.models import Director, Voter  # Import your Voter model after Django is initialized

# # Load known face(s) and encode them
# print("Loading known faces from the database...")
# voters = Director.objects.all()  # Query all voter objects
# known_face_encodings = []
# known_face_names = []

# for voter in voters:
#     image_path = voter.image.path  # Get the full file path for the image
#     print(f"Processing {image_path} for {voter.first_name}")
#     known_image = face_recognition.load_image_file(image_path)
#     known_encoding = face_recognition.face_encodings(known_image)
#     if known_encoding:
#         known_face_encodings.append(known_encoding[0])  # Use the first face encoding
#         known_face_names.append(voter.first_name)  # Save the voter's name
#     else:
#         print(f"Warning: No face detected in {image_path}")

# # Initialize the video capture
# video_capture = cv2.VideoCapture(0)  # Default webcam
# print("Starting real-time face recognition... Press 'q' to quit.")

# while True:
#     # Capture a single frame from the webcam
#     ret, frame = video_capture.read()
#     if not ret:
#         print("Failed to grab frame. Exiting...")
#         break

#     # Convert the frame from BGR (OpenCV) to RGB (face_recognition uses RGB)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Find all face locations and encodings in the current frame
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     # List for storing names of detected faces
#     face_names = []

#     for face_encoding in face_encodings:
#         # Compare the current face with the known faces
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
#         name = "Unknown"  # Default to "Unknown"

#         if True in matches:
#             # Find the index of the first match
#             match_index = matches.index(True)
#             name = known_face_names[match_index]

#     face_names.append(name)

#     # Draw rectangles and labels around the detected faces
#     for (top, right, bottom, left), name in zip(face_locations, face_names):
#         # Draw a rectangle around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

#         # Draw a label with the name below the rectangle
#         cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

#     # Display the resulting frame
#     cv2.imshow("Video", frame)

#     # Press 'q' to quit
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# # Release the webcam and close the window
# video_capture.release()
# cv2.destroyAllWindows()







# import cv2

# # Enable OpenCL for AMD GPU
# cv2.ocl.setUseOpenCL(True)
# cv2.ocl.useOpenCL(True)


# # Load pre-trained face detection model
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # Start webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Convert frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#     # Draw rectangles around detected faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
#     # Display the frame
#     cv2.imshow("Face Detection", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()









# import cv2
# import numpy as np


# # Enable OpenCL for AMD GPU
# cv2.ocl.setUseOpenCL(True)
# if not cv2.ocl.useOpenCL():
#     raise RuntimeError("OpenCL is not enabled in OpenCV. Ensure AMD drivers and OpenCL are installed.")

# # Load the Haar Cascade model for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # Load pre-trained LBPH face recognizer
# recognizer = cv2.face.LBPHFaceRecognizer()

# # Train the recognizer with sample faces (example setup)
# # Known face labels and images
# known_faces = [
#     {"label": 1, "image_path": "person1.jpg", "name": "Person 1"},
#     {"label": 2, "image_path": "person2.webp", "name": "Person 2"}
# ]


# # Prepare training data
# training_images = []
# labels = []
# names = {}

# for face in known_faces:
#     img = cv2.imread(face["image_path"], cv2.IMREAD_GRAYSCALE)
#     training_images.append(img)
#     labels.append(face["label"])
#     names[face["label"]] = face["name"]

# for i, img in enumerate(training_images):
#     print(img)
#     if img is None:
#         raise ValueError(f"Training image {i} failed to load. Check the file paths.")
#     if img.dtype != np.uint8:
#         raise ValueError(f"Training image {i} is not in the correct format (np.uint8).")


# labels = np.array(labels, dtype=np.int32)


# # Train the recognizer
# recognizer.train(training_images, np.array(labels))

# # Start webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to grayscale for processing
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#     for (x, y, w, h) in faces:
#         # Extract the face region
#         face_roi = gray[y:y+h, x:x+w]

#         # Recognize the face
#         label, confidence = recognizer.predict(face_roi)
#         name = names.get(label, "Unknown")

#         # Draw a rectangle and label around the face
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         cv2.putText(frame, f"{name} ({confidence:.2f})", (x, y-10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#     # Display the frame
#     cv2.imshow("Face Detection and Recognition (AMD GPU)", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()






# import cv2
# import numpy as np

# # Enable OpenCL for AMD GPU
# # cv2.ocl.setUseOpenCL(True)
# # if not cv2.ocl.useOpenCL():
# #     raise RuntimeError("OpenCL is not enabled in OpenCV. Ensure AMD drivers and OpenCL are installed.")

# # Load the Haar Cascade model for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # Load pre-trained LBPH face recognizer
# recognizer = cv2.face.LBPHFaceRecognizer_create()

# # Known face labels and images
# known_faces = [
#     {"label": 1, "image_path": "person1.jpg", "name": "Person 1"},
#     {"label": 2, "image_path": "person2.webp", "name": "Person 2"}
# ]

# # Prepare training data
# training_images = []
# labels = []
# names = {}

# # Fixed dimensions for training images
# IMG_SIZE = (150, 150)

# for face in known_faces:
#     img = cv2.imread(face["image_path"])
#     if img is None:
#         raise ValueError(f"Failed to load image: {face['image_path']}")
    
#     # if len(img.shape) == 3:  # Check for color channels
#     #     print("Gray")

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Resize to fixed size
#     img = cv2.resize(img, IMG_SIZE)
#     training_images.append(img)
#     labels.append(face["label"])
#     names[face["label"]] = face["name"]

# # print(len(training_images))

# # Convert labels to a NumPy array
# labels = np.array(labels, dtype=np.int32)
# # print(len(labels))

# # Train the recognizer
# recognizer.train(training_images, labels)

# # Start webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to grayscale for processing
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#     for (x, y, w, h) in faces:
#         # Extract the face region
#         face_roi = gray[y:y+h, x:x+w]

#         # Resize face ROI to match training image size
#         face_roi_resized = cv2.resize(face_roi, IMG_SIZE)

#         # Recognize the face
#         label, confidence = recognizer.predict(face_roi_resized)
#         name = names.get(label, "Unknown")

#         # Draw a rectangle and label around the face
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         cv2.putText(frame, f"{name} ({confidence:.2f})", (x, y-10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#     # Display the frame
#     cv2.imshow("Face Detection and Recognition (AMD GPU)", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()














# import cv2
# import dlib
# import numpy as np

# cv2.ocl.setUseOpenCL(True)

# # Load dlib's face detector and pre-trained face recognition model
# detector = dlib.get_frontal_face_detector()
# sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib's model repository
# face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # Pretrained model

# # Known face embeddings and labels (Example: You can add more known faces)
# known_face_encodings = []
# known_face_names = []

# # Example: Add known faces
# def add_known_face(image_path, name):
#     img = cv2.imread(image_path)
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     faces = detector(img_rgb)

#     if len(faces) == 0:
#         print(f"No face found in {image_path}")
#         return

#     shape = sp(img_rgb, faces[0])
#     face_encoding = np.array(face_rec_model.compute_face_descriptor(img_rgb, shape))
#     known_face_encodings.append(face_encoding)
#     known_face_names.append(name)

# # Add known faces here
# add_known_face("person1.jpg", "Person 1")
# add_known_face("person2.webp", "Person 2")

# # Start webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to RGB (required for dlib)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Detect faces in the frame
#     faces = detector(rgb_frame)

#     for face in faces:
#         # Get facial landmarks
#         shape = sp(rgb_frame, face)

#         # Generate the face encoding for the detected face
#         face_encoding = np.array(face_rec_model.compute_face_descriptor(rgb_frame, shape))

#         # Compare with known faces
#         matches = []
#         for known_encoding in known_face_encodings:
#             # Use Euclidean distance for comparison
#             distance = np.linalg.norm(face_encoding - known_encoding)
#             matches.append(distance)

#         # Find the best match
#         if len(matches) > 0:
#             best_match_index = np.argmin(matches)
#             if matches[best_match_index] < 0.6:  # Threshold for recognition
#                 name = known_face_names[best_match_index]
#             else:
#                 name = "Unknown"
#         else:
#             name = "Unknown"

#         # Draw a rectangle around the face and label it
#         x, y, w, h = (face.left(), face.top(), face.width(), face.height())
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     # Display the frame
#     cv2.imshow("Face Recognition", frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()

