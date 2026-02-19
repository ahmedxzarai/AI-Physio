<div align="center">
  <h1>🧬 AI-Physio</h1>
  <p><b>Real-Time Biomechanical Squat Analysis & Kinematic Intelligence</b></p>

  ![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg?style=for-the-badge&logo=python&logoColor=white)
  ![MediaPipe](https://img.shields.io/badge/MediaPipe-0081FB?style=for-the-badge&logo=google&logoColor=white)
  ![Status](https://img.shields.io/badge/Build-Production--Ready-brightgreen?style=for-the-badge)
  ![License](https://img.shields.io/badge/license-MIT-weight.svg?style=for-the-badge)

  <p><i>High-performance biomechanical engine quantifying human movement through Computer Vision and 3D coordinate extraction.</i></p>
</div>

---

### 📌 Abstract
*AI-Physio* is a clinical-grade biomechanical analysis engine. By leveraging the *MediaPipe Tasks API*, the system performs real-time extraction of 33 anatomical landmarks. Utilizing a *Finite-State Machine (FSM)*, it enforces strict Range-of-Motion (ROM) constraints to provide precision feedback for athletic performance and physical rehabilitation.

### 🧠 Core Technical Architecture
The system operates on a modular inference pipeline:

* *Landmark Acquisition:* Sub-30ms latency inference using MediaPipe Pose Landmarker.
* *Kinematic Modeling:* Trigonometric vector analysis to calculate the interior angle of the knee joint.
    * The angle $\theta$ is derived using the Law of Cosines on the 3D vectors $\vec{a}$ (hip-to-knee) and $\vec{b}$ (knee-to-ankle):
    $$\theta = \arccos\left(\frac{\vec{a} \cdot \vec{b}}{|\vec{a}| |\vec{b}|}\right)$$
* *State Machine Logic:* A robust FSM tracks transitions between UP and DOWN states.
* *Data Telemetry:* Automatic serialization of session data into `JSON`/`CSV` for longitudinal tracking.

---

### 🎯 Key Features
* *Real-Time Joint Analytics:* Live UI overlay with color-coded depth feedback.
* *Session Persistence:* Automated logging of peak extension/flexion and rep duration.
* *Production Standards:* Fully type-hinted Python 3.13 source code following *PEP 8*.
* *Hardware Agnostic:* Robust environment checks for CPU/GPU model availability.

---

### 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| *Inference Engine* | MediaPipe Tasks API |
| *Logic Layer* | Python 3.13 (Finite-State Machine) |
| *Math Engine* | NumPy / Vector Calculus |
| *Visuals* | OpenCV (High-FPS Overlay) |
| *Data Format* | JSON / CSV Telemetry |

---

### 📦 Project Structure
```text
AI-Physio/
├── main.py                # System Entry Point & Logic
├── utils/                 # Kinematic Math & Processing
├── models/                # pose_landmarker.task
├── requirements.txt       # Optimized for Python 3.13
├── README.md              # Project Documentation
└── LICENSE                # MIT License
```

### 🖥 Installation & Setup
<details>
<summary><b>View Implementation Guide (Click to Expand)</b></summary>


1. Clone the repository
```bash
git clone https://github.com/ahmedxzarai/AI-Physio.git
cd AI-Physio
```
2. Environment Configuration
```bash
pip install -r requirements.txt
```
3. Download AI Model
```text
Download the Pose Landmarker Task and place it in the root folder as pose_landmarker.task.
```
4. Execution
```bash
python main.py
```
</details>

### 📈 Data Insights (Telemetry Output)
The engine generates a summary_session.json after every cycle:
```json
{
  "total_valid_reps": 15,
  "avg_knee_angle": 102.4,
  "min_depth_angle": 88.2,
  "session_duration_sec": 45.3
}
```

### 👤 Author
**AHMED ZARAI**<br>
*AI Systems & Biometric Intelligence Developer*





<div align="center">
<p>Copyright © 2026 AHMED ZARAI. Distributed under the MIT License.</p>
</div>