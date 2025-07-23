# src/detection_utils.py
from ultralytics import YOLO
import cv2
import numpy as np
from src.tracker_utils import update_tracker

# Chargement du modèle YOLOv5 (u = version améliorée)
model = YOLO("yolov5su.pt")  # tu peux aussi utiliser 'yolov5s.pt' si tu préfères

class StaticObjectDetector:
    def __init__(self, threshold=5000, static_frames_threshold=30):
        self.back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50)
        self.static_frames_threshold = static_frames_threshold
        self.object_tracks = {}  # bbox -> compteur de frames
        self.threshold = threshold

    def detect_static_objects(self, frame):
        """
        Détecte les objets statiques en comparant avec l'arrière-plan.
        Renvoie une liste de bounding boxes (x1, y1, x2, y2)
        """
        fg_mask = self.back_sub.apply(frame)
        _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        static_boxes = []
        for cnt in contours:
            if cv2.contourArea(cnt) > self.threshold:
                x, y, w, h = cv2.boundingRect(cnt)
                static_boxes.append((x, y, x + w, y + h))

        return static_boxes


def detect_persons(frame):
    """
    Détection des personnes uniquement (pas de tracking).
    Retourne : frame annoté, nombre de personnes, liste des bounding boxes
    """
    results = model(frame)[0]
    person_boxes = []
    annotated_frame = frame.copy()
    count = 0

    for box in results.boxes:
        cls = int(box.cls[0])
        if model.names[cls] == 'person':
            count += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            person_boxes.append((x1, y1, x2, y2))
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, "person", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return annotated_frame, count, person_boxes


def track_persons(frame):
    """
    Détecte les personnes avec YOLO et les suit avec le tracker SORT.
    Retourne : frame annoté, liste [(x1,y1,x2,y2,ID), ...]
    """
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        if model.names[cls] == 'person':
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append([x1, y1, x2, y2, conf])

    tracked_boxes = update_tracker(detections, frame)

    return frame.copy(), tracked_boxes  # chaque élément : (x1, y1, x2, y2, ID)
