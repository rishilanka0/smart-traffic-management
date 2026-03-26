import cv2
import numpy as np
from ultralytics import YOLO
from config import MODEL_PATH

model = YOLO(MODEL_PATH)

def detect(frame):

    results = model(frame, conf=0.15, imgsz=960)[0]

    boxes = results.boxes.xyxy.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy()

    detections = []
    ambulance = False

    for (x1, y1, x2, y2), cls in zip(boxes, classes):

        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        label = model.names[int(cls)]

        # 🚑 ambulance detection
        if isinstance(label, str) and label.lower() == "emergency vechile":
            ambulance = True

        # ✅ keep EVERYTHING
        detections.append([x1, y1, x2, y2, label])

    return frame, detections, ambulance