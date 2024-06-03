from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import cv2
from ultralytics import YOLO
import random
import time
from collections import deque

# Load YOLO model
model = YOLO('yolov5nu.pt')
model.info()

# Define colors for different classes
COLORS = {}
for i in range(0, 80):
    COLORS[i] = [random.randint(0, 255) for _ in range(3)]

# Feed status and history of identified items
class FeedStatus:
    paused = False
    identified_items_history = deque(maxlen=25)
    current_items = []

def gen_frames(source=0):
    cap = cv2.VideoCapture(source)  # Capture from webcam or video
    while True:
        if FeedStatus.paused:
            time.sleep(0.1)
            continue

        success, frame = cap.read()  # Read frame
        if not success:
            break
        else:
            # Mirror the image
            frame = cv2.flip(frame, 1)

            FeedStatus.current_items.clear()  # Clear current items list
            results = model(frame)  # Perform YOLO on frame
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    color = COLORS[cls]

                    FeedStatus.identified_items_history.appendleft(label)  # Add to history
                    FeedStatus.current_items.append(label)

                    # Draw bounding boxes and labels
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(0), content_type='multipart/x-mixed-replace; boundary=frame')

def video_file_feed(request):
    video_path = 'path/to/your/video.mp4'  # Replace with your video file path
    return StreamingHttpResponse(gen_frames(video_path), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    identified_items_history = list(FeedStatus.identified_items_history)  # Convert deque to list
    current_items = list(FeedStatus.current_items)  # Convert to a list
    return render(request, 'home.html', {
        'identified_items_history': identified_items_history,
        'current_items': current_items
    })

def control_feed(request, action):
    if action == 'pause':
        FeedStatus.paused = True
    elif action == 'resume':
        FeedStatus.paused = False
    elif action == 'reload':
        FeedStatus.paused = False  # Reload is like resume, so we unpause it
    return JsonResponse({'status': 'ok'})
