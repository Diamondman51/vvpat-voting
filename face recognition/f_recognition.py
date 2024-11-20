import cv2
import face_recognition
from face_recognition import face_locations, face_encodings

# we'll create empty lists for voters faces' encodings and their names
voters_face_encodings = []
voters_names = []

# loading voters' images
voter1_image = face_recognition.load_image_file('voter1.jpg')
voter2_image = face_recognition.load_image_file('voter2.jpg')
voter3_image = face_recognition.load_image_file('voter3.jpg')
voter4_image = face_recognition.load_image_file('voter4.jpg')

# encoding voters' images
voter1_encoding = face_recognition.face_encodings(voter1_image)[0]
voter2_encoding = face_recognition.face_encodings(voter2_image)[0]
voter3_encoding = face_recognition.face_encodings(voter3_image)[0]
voter4_encoding = face_recognition.face_encodings(voter4_image)[0]

# this adds each encoding into voters faces' encodings list earlier created
voters_face_encodings.append(voter1_encoding)
voters_face_encodings.append(voter2_encoding)
voters_face_encodings.append(voter3_encoding)
voters_face_encodings.append(voter4_encoding)

# this adds each name into voters' names list earlier created
voters_names.append('Name of voter1')
voters_names.append('Name of voter2')
voters_names.append('Name of voter3')
voters_names.append('Name of voter4')

# Initializing webcam
video_capture = cv2.VideoCapture(0)

while True:
    # frame capturing
    ret, frame = video_capture.read()

    # finding face locations in the frame
    f_locations = face_recognition.face_locations(frame)
    f_encodings = face_recognition.face_encodings(frame, f_locations)

    # looping through each face founded in the frame
    for (top, right, bottom, left), f_encoding in zip(f_locations, f_encodings):
        # checking if the face matches any voters face
        matches = face_recognition.compare_faces(voters_face_encodings, f_encoding)
        name = 'Unknown'

        if True in matches:
            match_index = matches.index(True)
            name = voters_names[match_index]

        # drawing rectangle around the face and labeling with the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left - 10, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # displaying the resulting frame
    cv2.imshow('Video', frame)

    # break the while loop when the key 'q' is pressed
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

