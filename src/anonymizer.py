# src/anonymizer.py
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def anonymize_faces(frame, excluded_zones=None):
    """
    Floute les visages détectés, sauf ceux qui sont dans excluded_zones (list of bounding boxes).

    Args:
        frame (numpy.ndarray): image BGR
        excluded_zones (list of (x1,y1,x2,y2)): zones à ne pas flouter (optionnel)

    Returns:
        frame_floutée (numpy.ndarray)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    annotated_frame = frame.copy()

    for (x, y, w, h) in faces:
        face_box = (x, y, x + w, y + h)
        # Ne pas flouter si intersecte une zone exclue
        if excluded_zones:
            if any(intersect_boxes(face_box, zone) for zone in excluded_zones):
                continue

        face_roi = annotated_frame[y:y+h, x:x+w]
        # Floutage Gaussian
        face_roi = cv2.GaussianBlur(face_roi, (51, 51), 30)
        annotated_frame[y:y+h, x:x+w] = face_roi

    return annotated_frame


def intersect_boxes(box1, box2):
    x11, y11, x12, y12 = box1
    x21, y21, x22, y22 = box2
    horizontal = (x11 <= x22) and (x12 >= x21)
    vertical = (y11 <= y22) and (y12 >= y21)
    return horizontal and vertical
