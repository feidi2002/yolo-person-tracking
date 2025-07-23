# src/zone_monitor.py
import cv2
import datetime
import os

class ZoneMonitor:
    def __init__(self, zones=None, output_dir="output", log_file="output/alerts.log"):
        """
        zones : liste de tuples (x1, y1, x2, y2) définissant les zones interdites
        output_dir : dossier où sauvegarder les captures d'alerte
        log_file : fichier de log des alertes
        """
        self.zones = zones if zones is not None else []
        self.output_dir = output_dir
        self.log_file = log_file
        os.makedirs(self.output_dir, exist_ok=True)
        # Création du fichier log s'il n'existe pas
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("Log des alertes de zones interdites\n")

    def is_inside_zone(self, box, zone):
        """
        Vérifie si la boîte box intersecte la zone interdite zone
        box, zone : tuple (x1, y1, x2, y2)
        """
        x1, y1, x2, y2 = box
        zx1, zy1, zx2, zy2 = zone
        # Test d'intersection entre 2 rectangles
        horizontal_overlap = (x1 <= zx2) and (x2 >= zx1)
        vertical_overlap = (y1 <= zy2) and (y2 >= zy1)
        return horizontal_overlap and vertical_overlap

    def check_intrusions(self, detections):
        """
        Vérifie si une des detections (list de boxes) entre dans une zone interdite

        detections : liste de tuples (x1,y1,x2,y2)

        Retourne True si intrusion détectée, sinon False
        """
        for box in detections:
            for zone in self.zones:
                if self.is_inside_zone(box, zone):
                    return True
        return False

    def annotate_frame(self, frame, detections):
        """
        Dessine les zones interdites et les boxes détectées.

        Détecte aussi les intrusions et ajoute un message si besoin.

        Renvoie :
          - frame annotée
          - flag alerte (bool)
        """
        alert_triggered = False

        # Dessiner zones interdites en rouge
        for zone in self.zones:
            zx1, zy1, zx2, zy2 = zone
            cv2.rectangle(frame, (zx1, zy1), (zx2, zy2), (0, 0, 255), 2)
            cv2.putText(frame, "Zone interdite", (zx1, zy1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Dessiner boxes des detections en vert
        for box in detections:
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Vérifier intrusion
        if self.check_intrusions(detections):
            alert_triggered = True
            cv2.putText(frame, "ALERTE : zone interdite !", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            # Sauvegarder la frame avec timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"alert_{timestamp}.jpg")
            cv2.imwrite(filename, frame)

            # Log
            with open(self.log_file, "a") as log_file:
                log_file.write(f"{timestamp} - Intrusion détectée\n")

        return frame, alert_triggered
