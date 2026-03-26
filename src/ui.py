import cv2
import time

# -------- DRAW DETECTION BOXES --------
def draw_boxes(frame, objects):

    for obj in objects:

        x1, y1, x2, y2 = obj[:4]

        # handle label safely
        label = obj[4] if len(obj) > 4 else "vehicle"

        # default color
        color = (0, 255, 0)

        # check if label is string before using .lower()
        if isinstance(label, str):
            if label.lower() == "ambulance":
                color = (0, 0, 255)
        else:
            # if it's ID (int)
            label = f"ID {label}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.putText(frame, str(label),
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, color, 2)


# -------- DRAW SIGNAL --------
def draw_signal(frame, signal, active):

    x, y = 40, 80

    # 🔥 default = RED for all lanes
    color = (0, 0, 255)
    text = "RED"

    if active:
        if signal == "GREEN":
            color = (0, 255, 0)
            text = "GREEN"
        elif signal == "YELLOW":
            color = (0, 255, 255)
            text = "YELLOW"

    # draw signal
    cv2.circle(frame, (x, y), 18, color, -1)

    # label
    cv2.putText(frame, text,
                (x + 30, y + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, color, 2)


# -------- DRAW STATS (COUNT + TIMER) --------
def draw_stats(frame, count, timer, active):

    # vehicle count
    cv2.rectangle(frame, (10, 10), (200, 60), (0, 0, 0), -1)

    cv2.putText(frame, f"Vehicles: {count}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    # 🔥 ONLY ACTIVE LANE SHOWS TIMER
    if active:
        h, w = frame.shape[:2]

        cv2.rectangle(frame, (w - 120, 10), (w - 10, 80), (255, 255, 255), -1)

        cv2.putText(frame, f"{int(timer):02d}",
                    (w - 105, 65),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1.5, (0, 0, 255), 3)

        cv2.putText(frame, "ACTIVE",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)


# -------- DRAW EMERGENCY --------
def draw_emergency(frame, is_emergency):

    if is_emergency:

        if int(time.time() * 2) % 2 == 0:

            cv2.rectangle(frame, (150, 10), (500, 70), (0, 0, 255), -1)

            cv2.putText(frame, "🚑 EMERGENCY",
                        (180, 55),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 3)