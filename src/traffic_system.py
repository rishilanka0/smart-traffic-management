import cv2
import numpy as np
from ultralytics import YOLO

# Load trained model
model = YOLO("D:\\SSDP\\traffic\\checkpoints\\best.pt")

# Load 4 traffic camera videos
cap1 = cv2.VideoCapture("D:\\SSDP\\traffic\\videos\\1.mp4")
cap2 = cv2.VideoCapture("D:\\SSDP\\traffic\\videos\\2.mp4")
cap3 = cv2.VideoCapture("D:\\SSDP\\traffic\\videos\\3.mp4")
cap4 = cv2.VideoCapture("D:\\SSDP\\traffic\\videos\\4.mp4")

# Example ROI for camera 1 (use your coordinates)
roi1 = np.array([
    [405,51],
    [835,44],
    [839,295],
    [411,285]
])

# Placeholder ROI for other cameras
roi2 = roi1
roi3 = roi1
roi4 = roi1


def detect_vehicles(frame, roi):

    results = model(frame, imgsz=960, conf=0.35)

    count = 0
    ambulance = False

    for r in results:
        boxes = r.boxes

        for box in boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            conf = float(box.conf[0])

            x1,y1,x2,y2 = map(int, box.xyxy[0])

            center_x = (x1+x2)//2
            center_y = (y1+y2)//2

            inside = cv2.pointPolygonTest(roi,(center_x,center_y),False)

            if inside < 0:
                continue

            count += 1

            color = (0,255,0)

            if label.lower() == "ambulance":
                color = (0,0,255)
                ambulance = True

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

            text = f"{label} {conf:.2f}"

            cv2.putText(frame,text,(x1,y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,color,2)

    cv2.polylines(frame,[roi],True,(255,0,0),2)

    return frame, count, ambulance


while True:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()

    if not ret1:
        break

    frame1, c1, amb1 = detect_vehicles(frame1, roi1)
    frame2, c2, amb2 = detect_vehicles(frame2, roi2)
    frame3, c3, amb3 = detect_vehicles(frame3, roi3)
    frame4, c4, amb4 = detect_vehicles(frame4, roi4)

    counts = [c1, c2, c3, c4]
    ambulances = [amb1, amb2, amb3, amb4]

    # Emergency priority
    if True in ambulances:
        green_lane = ambulances.index(True)
    else:
        green_lane = counts.index(max(counts))

    states = ["RED","RED","RED","RED"]
    states[green_lane] = "GREEN"

    frames = [frame1,frame2,frame3,frame4]

    for i,f in enumerate(frames):

        text = f"Vehicles: {counts[i]}"

        cv2.putText(f,text,(20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,255,0),2)

        signal = states[i]

        color = (0,0,255)

        if signal == "GREEN":
            color = (0,255,0)

        cv2.circle(f,(40,80),15,color,-1)

        cv2.putText(f,signal,(70,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,color,2)

    # Create dashboard
    # resize frames to same size
    frame1 = cv2.resize(frame1,(640,360))
    frame2 = cv2.resize(frame2,(640,360))
    frame3 = cv2.resize(frame3,(640,360))
    frame4 = cv2.resize(frame4,(640,360))

    top = cv2.hconcat([frame1,frame2])
    bottom = cv2.hconcat([frame3,frame4])

    dashboard = cv2.vconcat([top,bottom])

    cv2.imshow("Smart Traffic Control System",dashboard)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap1.release()
cap2.release()
cap3.release()
cap4.release()

cv2.destroyAllWindows()