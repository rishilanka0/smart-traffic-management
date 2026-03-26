import numpy as np
import supervision as sv

tracker = sv.ByteTrack()

def track(detections):

    if len(detections) == 0:
        return []

    boxes = []
    confidences = []
    class_ids = []

    for d in detections:

        x1,y1,x2,y2,label = d

        boxes.append([x1,y1,x2,y2])

        confidences.append(0.9)   # placeholder confidence
        class_ids.append(0)

    boxes = np.array(boxes)
    confidences = np.array(confidences)
    class_ids = np.array(class_ids)

    sv_det = sv.Detections(
        xyxy=boxes,
        confidence=confidences,
        class_id=class_ids
    )

    tracked = tracker.update_with_detections(sv_det)

    if tracked.tracker_id is None:
        return []

    tracked_objects = []

    for box,tid in zip(tracked.xyxy,tracked.tracker_id):

        x1,y1,x2,y2 = map(int,box)

        tracked_objects.append((x1,y1,x2,y2,int(tid)))

    return tracked_objects