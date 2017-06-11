from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import os

# Block beacon by default
unitBlocked = "blocked"

# Get the Cascade Classifier for the Computer Vision
cascPath = "cars.xml"
haarCascade = cv2.CascadeClassifier(cascPath)

# Stream the camera
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 50)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Make it gray for better analytics
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Fetch detected objects
    detections = haarCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the objects
    for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Is there an object?
    if getattr(detections, 'size', len(detections)):
	print "Found one! Block the unit!"
	unitBlocked = "blocked"
    else:
        unitBlocked = "free"
	print "Nothing found yet. Unblock it and go!"

    # Push the state to the Arduino!
    os.system("sudo python sendArduinoOnce.py "+unitBlocked)

    # Display the resulting frame (for DEV supposes)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
