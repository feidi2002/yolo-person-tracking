# main.py
import cv2
from src.detection_utils import track_persons, StaticObjectDetector
from src.zone_monitor import ZoneMonitor
from src.anonymizer import anonymize_faces

# Zones interdites
forbidden_zones = [
    (100, 50, 300, 400),
]

# Initialisation des modules
zone_monitor = ZoneMonitor(zones=forbidden_zones)
static_detector = StaticObjectDetector()

# Paramètres de détection statique
STATIC_OBJECT_TIME_THRESHOLD = 30
static_object_last_boxes = []
static_object_frames_count = 0

def run_video(source=0):
    global static_object_last_boxes, static_object_frames_count

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la source vidéo.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détection + Tracking des personnes
        frame, tracked_persons = track_persons(frame)

        # Récupération des bounding boxes seules (pour zone_monitor et anonymisation)
        person_boxes = [(x1, y1, x2, y2) for x1, y1, x2, y2, _id in tracked_persons]

        # Détection objets statiques
        static_boxes = static_detector.detect_static_objects(frame)
        if static_boxes == static_object_last_boxes and static_boxes:
            static_object_frames_count += 1
        else:
            static_object_frames_count = 0
        static_object_last_boxes = static_boxes

        if static_object_frames_count >= STATIC_OBJECT_TIME_THRESHOLD:
            for box in static_boxes:
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                cv2.putText(frame, "Objet statique détecté", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Affichage ID pour chaque personne détectée
        for (x1, y1, x2, y2, pid) in tracked_persons:
            cv2.putText(frame, f"ID {pid}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Surveillance zones interdites
        frame, alert = zone_monitor.annotate_frame(frame, person_boxes)

        # Anonymisation des visages (hors zones interdites)
        frame = anonymize_faces(frame, excluded_zones=forbidden_zones)

        # Affichage du nombre de personnes détectées
        cv2.putText(frame, f'Personnes : {len(tracked_persons)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Surveillance complète", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Choisissez la source :")
    print("1 - Webcam")
    print("2 - Vidéo locale")
    choix = input("Votre choix (1/2) : ")
    if choix == "1":
        run_video(0)
    elif choix == "2":
        run_video("data/video_test.mp4")
    else:
        print("Choix non reconnu.")
 