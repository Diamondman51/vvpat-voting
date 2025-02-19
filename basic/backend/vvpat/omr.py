import json
import cv2
from pyzbar import pyzbar

import os
import sys
import django
import cv2

# Setup Django environment
sys.path.append(r'E:/vvpat-voting/basic/backend')  # Add your Django project directory to the Python path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")  # Use the correct settings module
django.setup()

from vvpat.models import Director, President, Voter


def read_qr_code(frame):
    # Decode QR codes in the frame
    qr_codes = pyzbar.decode(frame)
    for qr in qr_codes:
        # Extract data from the QR code
        qr_data = qr.data.decode('utf-8')

        # Get coordinates of the QR code box
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display QR code data and type
        text = f'{qr_data}'

        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 2)

        json_data = json.loads(text)
        try:    
            user_id = json_data.get('user_id')

            president_id = json_data.get('president_id')
            selected_directors = json_data.get('selected_directors')

            try:
                president = President.objects.get(id=president_id)
                if not hasattr(President, 'count'):
                    president.count = 0
            except President.DoesNotExist:
                president = None

            if president and user_id not in president.omr_votes:
                president.count += 1
                president.omr_votes.append(user_id)
                president.save()
                print(f'Voted for {president.first_name} {president.last_name}')

            for director_id in selected_directors:
                try:
                    director = Director.objects.get(id=director_id)
                    if not hasattr(Director, 'count'):
                        director.count = 0
                except Director.DoesNotExist:
                    director = None

                if director and user_id not in director.omr_votes:
                    director.count += 1
                    director.omr_votes.append(user_id)
                    director.save()
                    print(f'Voted for {director.first_name} {director.last_name}')

        except Exception as e:
            print(e)

    #TODO Add field dynamically, to the json add voters id, it is need for counting votes

    # Save the votes to the database

    return frame, qr_codes

def main():
    # Open the camera (0 is the default camera)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame to read QR codes
        frame, qr_codes = read_qr_code(frame)

        # Display the frame with QR code data
        cv2.imshow('QR Code Scanner', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

