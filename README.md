🎥 Video Surveillance System with Anonymization and Tracking
A Python-based video surveillance system that detects, tracks, and logs people moving through defined zones in a video feed. It also provides a GUI to control anonymization settings in real time.

🧠 Features
🧍‍♂️ Person detection using YOLOv5s (custom-trained with yolov5su)

🎯 Real-time tracking with SORT

🔐 Optional face anonymization (blurring or pixelation)

📍 Zone-based movement logging

🖥️ Control panel GUI for live interaction

📁 Supports both live webcam and video files

📂 Project Structure
bash
Copy
Edit
.
├── main.py                # Entry point of the application
├── anonymizer.py          # Face anonymization logic
├── control_panel.py       # GUI to control options
├── detection_utils.py     # Wrapper for YOLOv5 detection
├── tracker_utils.py       # SORT tracker integration
├── video_utils.py         # Video input/output handling
├── zone_logger.py         # Logging person entries/exits in zones
├── zone_monitor.py        # Defines and monitors spatial zones
├── yolov5su/              # Your custom YOLOv5 fork
│   └── ...                # YOLOv5 model and training files
├── sort/                  # SORT tracker code
│   └── ...                # Kalman filter and bounding box tracker
├── requirements.txt       # Python dependencies
├── README.md              # This file
🚀 Getting Started
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/votre-nom/video-surveillance-anonymizer.git
cd video-surveillance-anonymizer
2. Install dependencies
Create a virtual environment if desired, then run:

bash
Copy
Edit
pip install -r requirements.txt
3. Download YOLOv5 weights
Put your trained weights (e.g. best.pt) in the yolov5su/weights/ directory.

Or train your own model:

bash
Copy
Edit
cd yolov5su
python train.py --img 640 --batch 16 --epochs 50 --data data.yaml --weights yolov5s.pt
4. Run the application
bash
Copy
Edit
python main.py
🖼️ Interface
Choose whether to anonymize faces

Select blur or pixelate mode

View zone logs in real time

Works with both live webcam and video files

🧪 Training Data Format
Your data.yaml should look like:

yaml
Copy
Edit
train: path/to/train/images
val: path/to/val/images
nc: 1
names: ['person']
✅ Requirements
Python 3.8+

OpenCV

PyTorch

PyYAML

Tkinter (built-in on most systems)

(See requirements.txt for full details)

📈 Future Features
Face recognition (optional whitelist)

Saving detection logs to CSV

Email alerts on entry

📄 License
MIT License. See LICENSE.
