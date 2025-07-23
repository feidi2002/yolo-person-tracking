# src/tracker_utils.py
from sort.sort import Sort
import numpy as np

tracker = Sort(max_age=100, min_hits=1, iou_threshold=0.2)

def update_tracker(detections, frame):
    """
    detections: list of bounding boxes [x1, y1, x2, y2, conf]
    Returns: list of tuples (x1, y1, x2, y2, id)
    """
    if len(detections) == 0:
        detections = np.empty((0, 5))
    else:
        detections = np.array(detections)

    tracked = tracker.update(detections)
    return [(int(x1), int(y1), int(x2), int(y2), int(track_id)) for x1, y1, x2, y2, track_id in tracked]
