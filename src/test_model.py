import cv2
import numpy as np
from ultralytics import YOLO

# Load trained model
model = YOLO("D:\\SSDP\\traffic\\runs\\detect\\train\\weights\\best.pt")

# Load video
cap = cv2.VideoCapture("D:\\SSDP\\traffic\\1.mp4")

# Emergency detection buffer
ambulance_frames = 0
AMBULANCE_CONFIRM_FRAMES = 5

# Vehicle classes
vehicle_classes = ["Car","Truck","Bus","Motorcycle","Ambulance"]

while True:

    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # ROI polygon (adjust if needed)
    roi_polygon = np.array([
    [405, 51],   # top-left near zebra crossing
    [835, 44],   # top-right
    [839, 295],  # bottom-right corner
    [411, 285]    # bottom-left
])
    # Draw ROI
    cv2.polylines(frame,[roi_polygon],True,(255,0,0),2)

    # Run detection (higher resolution improves motorcycle detection)
    results = model(frame, imgsz=960)

    vehicle_count = 0
    ambulance_detected = False

    for r in results:
        boxes = r.boxes

        for box in boxes:

            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            if label not in vehicle_classes:
                continue

            x1,y1,x2,y2 = map(int,box.xyxy[0])

            width = x2 - x1
            height = y2 - y1

            # Remove tiny detections
            if width < 25 or height < 25:
                continue

            center_x = int((x1+x2)/2)
            center_y = int((y1+y2)/2)

            # Check if inside ROI
            inside = cv2.pointPolygonTest(roi_polygon,(center_x,center_y),False)

            if inside < 0:
                continue

            # Draw bounding box
            color = (0,255,0)

            if label == "Ambulance":
                color = (0,0,255)

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
            cv2.putText(frame,label,(x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,color,2)

            # Count vehicles
            vehicle_count += 1

            # Ambulance detection (higher confidence required)
            if label == "Ambulance" and conf > 0.65:
                ambulance_detected = True

    # Emergency confirmation buffer
    if ambulance_detected:
        ambulance_frames += 1
    else:
        ambulance_frames = 0

    emergency = False

    if ambulance_frames >= AMBULANCE_CONFIRM_FRAMES:
        emergency = True

    # Display vehicle count
    cv2.putText(frame,f"Vehicles: {vehicle_count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),2)

    # Display emergency alert
    if emergency:
        cv2.putText(frame,"EMERGENCY VEHICLE DETECTED",
                    (200,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,0,255),3)

    cv2.imshow("Traffic Detection",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()