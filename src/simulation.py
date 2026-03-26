import cv2
import numpy as np
import time

WIDTH, HEIGHT = 800, 800

def draw_simulation(queues, lane, signal, timer, ambulances):

    img = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 210

    # -------- ROADS --------
    cv2.rectangle(img, (300, 0), (500, 800), (50,50,50), -1)
    cv2.rectangle(img, (0, 300), (800, 500), (50,50,50), -1)

    # -------- SIGNAL LIGHTS --------
    positions = [
        (260, 330),
        (430, 260),
        (540, 430),
        (330, 540)
    ]

    for i, (x, y) in enumerate(positions):

        color = (0,0,255)  # RED default

        if i == lane:
            if signal == "GREEN":
                color = (0,255,0)
            elif signal == "YELLOW":
                color = (0,255,255)

        cv2.circle(img, (x, y), 20, color, -1)

    # -------- CENTER TIMER (BIG & CLEAR) --------
    cv2.circle(img, (400, 400), 80, (255,255,255), -1)

    cv2.putText(img, f"{int(timer):02d}",
                (355, 430),
                cv2.FONT_HERSHEY_DUPLEX,
                2.5, (0,0,0), 4)

    # -------- ACTIVE LANE --------
    cv2.putText(img, f"Lane {lane+1} ACTIVE",
                (280, 500),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9, (0,0,0), 3)

    # -------- VEHICLE COUNTS (CLEAR BOXES) --------
    labels = ["Lane 1", "Lane 2", "Lane 3", "Lane 4"]

    box_positions = [
        (50, 320),
        (300, 40),
        (600, 320),
        (300, 700)
    ]

    for i, (x, y) in enumerate(box_positions):

        # box
        cv2.rectangle(img, (x-20, y-30), (x+180, y+20), (0,0,0), -1)

        # text
        cv2.putText(img, f"{labels[i]}: {queues[i]}",
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255,255,255), 2)

    # -------- SIGNAL STATUS --------
    cv2.putText(img, f"Signal: {signal}",
                (300, 600),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0,0,0), 2)

    # -------- EMERGENCY --------
    if True in ambulances:

        if int(time.time()*2) % 2 == 0:
            cv2.rectangle(img, (150, 30), (650, 100), (0,0,255), -1)

            cv2.putText(img, "🚑 EMERGENCY PRIORITY",
                        (180, 85),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255,255,255), 3)

    # -------- TITLE --------
    cv2.putText(img, "SMART TRAFFIC DASHBOARD",
                (180, 770),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (50,50,50), 2)

    return img