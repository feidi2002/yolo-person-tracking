# src/control_panel.py
import tkinter as tk

class ControlPanel:
    def __init__(self, root):
        self.detect_persons = tk.BooleanVar(value=True)
        self.detect_static = tk.BooleanVar(value=True)
        self.anonymize_faces = tk.BooleanVar(value=True)

        tk.Checkbutton(root, text="Détection de personnes", variable=self.detect_persons).pack(anchor="w")
        tk.Checkbutton(root, text="Détection objets statiques", variable=self.detect_static).pack(anchor="w")
        tk.Checkbutton(root, text="Anonymisation des visages", variable=self.anonymize_faces).pack(anchor="w")