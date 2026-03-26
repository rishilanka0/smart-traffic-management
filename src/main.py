import cv2
import time
from config import VIDEO_PATHS
from detector import detect
from tracker import track
from queue_estimator import estimate_queue
from rl_agent import RLAgent
from signal_controller import SignalController

# ✅ UI
from ui import draw_boxes, draw_signal, draw_stats, draw_emergency

caps = [cv2.VideoCapture(v) for v in VIDEO_PATHS]

agent = RLAgent()
controller = SignalController()

while True:

    frames = []
    queues = []
    ambulances = []

    # -------- PROCESS EACH CAMERA --------
    for cap in caps:

        ret, frame = cap.read()

        if not ret:
            break

        frame, dets, amb = detect(frame)

        objs = track(dets)

        q = estimate_queue(objs)

        draw_boxes(frame, objs)

        frames.append(frame)
        queues.append(q)
        ambulances.append(amb)

    if len(frames) < 4:
        break

    # -------- RL DECISION --------
    state = tuple(queues)

    action = agent.choose_action(state)

    reward = -sum(queues)

    agent.update(state, action, reward, state)

    # -------- SIGNAL CONTROL --------
    lane, signal, timer = controller.update(queues, ambulances, action)

    # -------- DRAW UI ON EACH CAMERA --------
    for i, f in enumerate(frames):

        # vehicle count + timer + active
        draw_stats(f, queues[i], timer, i == lane)

        # traffic signal
        draw_signal(f, signal, i == lane)

        # emergency alert
        draw_emergency(f, ambulances[i])

    # -------- DASHBOARD --------
    frames = [cv2.resize(f, (640, 360)) for f in frames]

    top = cv2.hconcat(frames[:2])
    bottom = cv2.hconcat(frames[2:])

    dashboard = cv2.vconcat([top, bottom])

    # -------- SHOW --------
    cv2.imshow("Smart Traffic AI System", dashboard)

    # -------- SPEED CONTROL --------
    time.sleep(0.03)

    if cv2.waitKey(1) == 27:
        break

# -------- CLEANUP --------
for cap in caps:
    cap.release()

cv2.destroyAllWindows()