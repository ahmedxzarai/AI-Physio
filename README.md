### AI-Physio: Real-Time Biomechanical Squat Analysis
Developed by AHMED ZARAI | 2026



### 📌 Abstract
AI-Physio is a high-performance biomechanical analysis engine designed to quantify human movement through Computer Vision. Built on the modern MediaPipe Tasks API, the system performs real-time 3D coordinate extraction of 33 anatomical landmarks to monitor joint kinematics. By utilizing a Finite-State Machine (FSM), the analyzer enforces strict range-of-motion (ROM) constraints, providing clinical-grade feedback for athletic performance and physical therapy.


### 🛠 Core Technical Architecture
The system follows a modular pipeline architecture:
- Landmark Acquisition: Leveraging the MediaPipe Pose Landmarker for sub-30ms latency inference.
- Kinematic Modeling: Implementing trigonometric vector analysis to calculate the interior angle of the knee joint (\\theta).
- State Machine Logic: A robust FSM tracks transitions between UP and DOWN states to ensure valid repetition counting.
- Data Telemetry: Automatic serialization of session data into CSV and JSON for longitudinal performance tracking.


### 🚀 Key Features
- Real-Time Joint Analytics: Live UI overlay of joint angles with color-coded depth feedback.
- Session Persistence: Automated logging of every rep, including duration and peak extension/flexion angles.
- Production-Ready Code: Fully type-hinted Python 3.13 source code following PEP 8 standards.
- Advanced Error Handling: Robust environment checks for model availability and webcam health.


### 🏗 Installation \& Setup

Clone the repository:
```bash
git clone https://github.com/ahmedxzarai/AI-Physio.git
cd AI-Physio
```

Environment Configuration:
Install dependencies (Optimized for Python 3.13):
```bash
pip install -r requirements.txt
```

Download AI Model: Download the Pose Landmarker Task and place it in the root folder as pose\_landmarker.task.

Execution:
```bash
python main.py
```


### 📈 Data Insights

The system generates a summary\_session.json after every workout, providing instant biomechanical feedback:
```text
{
"total\_valid\_reps": 15,
"avg\_knee\_angle": 102.4,
"min\_depth\_angle": 88.2,
"session\_duration\_sec": 45.3
}
```



### 📜 License \& Copyright
Copyright © 2026 AHMED ZARAI. Distributed under the MIT License. See LICENSE for more information.
