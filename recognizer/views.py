from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2
from ultralytics import YOLO
import random

# Load the YOLO model
model = YOLO('yolov5nu.pt')
model.info()

# Define colors for different classes
COLORS = {}
for i in range(0, 80):
    COLORS[i] = [random.randint(0, 255) for _ in range(3)]

def gen_frames():
    cap = cv2.VideoCapture(0)  # Capture from the webcam
    while True:
        success, frame = cap.read()  # Read a frame
        if not success:
            break
        else:
            results = model(frame)  # Run YOLO on the frame
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    color = COLORS[cls]

                    # Draw bounding boxes and labels
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request, 'home.html')
