from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import cv2
from ultralytics import YOLO
import random
import time

# Завантаження моделі YOLO
model = YOLO('yolov5nu.pt')
model.info()

# Визначення кольорів для різних класів
COLORS = {}
for i in range(0, 80):
    COLORS[i] = [random.randint(0, 255) for _ in range(3)]

# Статус паузи
class FeedStatus:
    paused = False

def gen_frames(source=0):
    cap = cv2.VideoCapture(source)  # Захоплення з веб-камери або відео
    while True:
        if FeedStatus.paused:
            time.sleep(0.1)
            continue

        success, frame = cap.read()  # Зчитування кадру
        if not success:
            break
        else:
            # Відзеркалення зображення
            frame = cv2.flip(frame, 1)
            
            results = model(frame)  # Виконання YOLO на кадрі
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    color = COLORS[cls]

                    # Малювання рамок і підписів
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(0), content_type='multipart/x-mixed-replace; boundary=frame')

def video_file_feed(request):
    video_path = 'path/to/your/video.mp4'  # Замініть на шлях до вашого відеофайлу
    return StreamingHttpResponse(gen_frames(video_path), content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request, 'home.html')

def control_feed(request, action):
    if action == 'pause':
        FeedStatus.paused = True
    elif action == 'resume':
        FeedStatus.paused = False
    elif action == 'reload':
        FeedStatus.paused = False  # Reload is like resume, so we unpause it
    return JsonResponse({'status': 'ok'})
