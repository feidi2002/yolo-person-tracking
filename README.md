# TI-VideoSurveillance

Détection, suivi et anonymisation de personnes dans des vidéos à l’aide de YOLOv5su et de l’algorithme SORT.

## 📌 Objectif

Ce projet permet de :
- Détecter des personnes dans une vidéo avec le modèle léger **YOLOv5su**
- Suivre chaque personne à l’aide du tracker **SORT**
- Anonymiser les visages (floutage ou pixellisation)
- Définir des **zones d’intérêt** et logguer les entrées/sorties
- Contrôler les paramètres via une interface graphique simple

## 🔧 Fonctionnalités

- 🔍 Détection en temps réel avec YOLOv5su (optimisé pour la vitesse)
- 🎯 Suivi d'identité avec le tracker SORT
- 🕵️‍♂️ Anonymisation automatique des visages
- 🗺️ Définition de zones personnalisées dans l’image
- 📋 Log des entrées/sorties par personne et par zone
- 🖥️ Interface de contrôle simple via une fenêtre tkinter

## 🗂️ Structure du projet

TIvideosurveillance/
├── main.py # Script principal
├── anonymizer.py # Floutage/pixellisation des visages
├── control_panel.py # Interface graphique pour les paramètres
├── detection_utils.py # Chargement et appel de YOLOv5su
├── tracker_utils.py # Initialisation et gestion du tracker SORT
├── video_utils.py # Lecture vidéo, écriture, affichage
├── zone_logger.py # Gestion des logs d'entrée/sortie
├── zone_monitor.py # Suivi des zones d’intérêt
├── yolov5/ # Dossier YOLOv5su (modèle + scripts nécessaires)
├── sort/ # Dossier contenant le tracker SORT
├── requirements.txt # Dépendances Python
└── README.md # Ce fichier
