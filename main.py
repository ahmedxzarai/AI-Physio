# ---------------------------------------------------------------------------
# Project: AI-Physio | Real-Time Biomechanical Squat Analysis System
# File:    main.py
# Author:  AHMED ZARAI
#
# Copyright (c) 2026 Ahmed Zarai. All rights reserved.
# ---------------------------------------------------------------------------

import cv2
import time
import csv
import json
import statistics
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

# Internal engine import
from pose_module import PoseDetector

# --- System Configuration ---
# Professional systems use configuration blocks for tunable parameters.
CONFIG = {
    "CAMERA_ID": 0,
    "FRAME_WIDTH": 1280,
    "FRAME_HEIGHT": 720,
    "MODEL_PATH": "pose_landmarker.task",
    # Biomechanical Thresholds
    "SQUAT_UP_THRESH": 165.0,   # Angle considered "standing straight"
    "SQUAT_DOWN_THRESH": 90.0,  # Angle considered "full depth"
    # Landmark Indices (MediaPipe standard)
    "LM_HIP": 24,
    "LM_KNEE": 26,
    "LM_ANKLE": 28
}
# ---------------------------

def main() -> None:
    """Main execution loop for the AI-Physio system."""
    
    # Initialize Video Capture
    cap = cv2.VideoCapture(CONFIG["CAMERA_ID"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["FRAME_WIDTH"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["FRAME_HEIGHT"])

    if not cap.isOpened():
        print(f"CRITICAL ERROR: Cannot access webcam ID {CONFIG['CAMERA_ID']}.")
        sys.exit(1)

    # Initialize the AI Engine
    try:
        detector = PoseDetector(model_path=CONFIG["MODEL_PATH"])
    except Exception as e:
        print(f"Failed to initialize AI engine: {e}")
        sys.exit(1)

    # State Machine Variables
    squat_count: int = 0
    squat_state: str = "UP" # Initial state
    
    # Session Metadata
    start_time_abs = time.time()
    session_id_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_telemetry: List[Dict[str, Any]] = []

    print(f"\n[System] Session {session_id_str} started.")
    print("[UI] Press 'q' in the window to terminate session and save data.\n")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[Warning] Failed to retrieve frame. Exiting.")
                break

            # --- 1. Process Frame ---
            timestamp_ms = int((time.time() - start_time_abs) * 1000)
            detector.detect(frame, timestamp_ms)
            landmarks = detector.get_landmarks(frame)

            current_session_time = time.time() - start_time_abs
            current_angle: Optional[float] = None

            # --- 2. Biomechanical Analysis ---
            if landmarks:
                # Extract 2D coordinates (ignoring ID at index 0)
                try:
                    hip_coords = landmarks[CONFIG["LM_HIP"]][1:]
                    knee_coords = landmarks[CONFIG["LM_KNEE"]][1:]
                    ankle_coords = landmarks[CONFIG["LM_ANKLE"]][1:]

                    current_angle = detector.calculate_angle(hip_coords, knee_coords, ankle_coords)

                    # Finite-State Machine (FSM) Logic for rep counting
                    if current_angle > CONFIG["SQUAT_UP_THRESH"]:
                        if squat_state == "DOWN":
                            squat_count += 1
                            print(f"[Action] Rep completed. Total: {squat_count}")
                        squat_state = "UP"
                    elif current_angle < CONFIG["SQUAT_DOWN_THRESH"]:
                        squat_state = "DOWN"
                        
                    # UI: Draw skeletal feedback
                    draw_biomechanics_ui(frame, knee_coords, current_angle, CONFIG["SQUAT_DOWN_THRESH"])

                except IndexError:
                    # Handle cases where limbs are temporarily out of frame
                    pass

            # --- 3. Telemetry Logging ---
            # Log every frame regardless of detection for complete time-series
            session_telemetry.append({
                "timestamp_sec": round(current_session_time, 3),
                "knee_angle_deg": round(current_angle, 2) if current_angle is not None else None,
                "fsm_state": squat_state,
                "cumulative_reps": squat_count
            })

            # --- 4. General UI Overlay ---
            draw_dashboard_ui(frame, squat_count, squat_state)

            # --- 5. Display & Exit Check ---
            cv2.imshow("AI-Physio | Engineering Prototype | Ahmed Zarai", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("\n[System] Termination signal received.")
                break

    except KeyboardInterrupt:
        print("\n[System] Session interrupted via keyboard.")

    finally:
        # Ensure resources are released and data is saved under any circumstance
        cap.release()
        cv2.destroyAllWindows()
        finalize_session(session_telemetry, session_id_str)


def draw_biomechanics_ui(frame, knee_coords, angle, threshold):
    """Helper to draw on-body angle feedback."""
    color = (0, 255, 0) # Green (good)
    if angle < threshold + 10: color = (0, 255, 255) # Yellow (approaching depth)
    if angle < threshold: color = (0, 0, 255) # Red (at depth)

    cv2.putText(frame, f"{int(angle)} deg", 
                (knee_coords[0] - 40, knee_coords[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

def draw_dashboard_ui(frame, count, state):
    """Helper to draw the main status dashboard."""
    # Background panel for UI readability
    cv2.rectangle(frame, (15, 15), (300, 130), (30, 30, 30), -1)
    cv2.rectangle(frame, (15, 15), (300, 130), (100, 100, 100), 2)
    
    # Metrics
    cv2.putText(frame, f"REPS: {count}", (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame, f"STATE: {state}", (30, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Branding
    cv2.putText(frame, "AI-Physio Eng. Sys.", (950, 30), 
                cv2.FONT_HERSHEY_PLAIN, 1, (150, 150, 150), 1, cv2.LINE_AA)


def finalize_session(telemetry_data: List[Dict[str, Any]], session_id: str) -> None:
    """Performs persistent data logging and statistical summarization."""
    
    if not telemetry_data:
        print("[Warning] No telemetry data collected. Skipping log generation.")
        return

    print("\n--- Finalizing Session Data ---")
    
    base_filename = f"session_log_{session_id}"
    csv_path = f"{base_filename}.csv"
    json_path = f"{base_filename}.json"

    # 1. Generate Time-Series CSV (for tabular analysis)
    try:
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=telemetry_data[0].keys())
            writer.writeheader()
            writer.writerows(telemetry_data)
        print(f"[IO] Time-series raw data saved to: {csv_path}")
    except IOError as e:
         print(f"[Error] Failed to write CSV: {e}")

    # 2. Generate Statistical Summary JSON (for application integration)
    valid_angles = [d["knee_angle_deg"] for d in telemetry_data if d["knee_angle_deg"] is not None]
    
    summary_stats = {
        "session_id": session_id,
        "engineer_credit": "Ahmed Zarai",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "metrics": {
            "total_duration_sec": telemetry_data[-1]["timestamp_sec"],
            "total_valid_reps": telemetry_data[-1]["cumulative_reps"],
            "biometrics": {
                "avg_knee_angle": round(statistics.mean(valid_angles), 2) if valid_angles else None,
                "min_depth_angle": round(min(valid_angles), 2) if valid_angles else None,
                "max_extension_angle": round(max(valid_angles), 2) if valid_angles else None
            }
        }
    }

    try:
        with open(json_path, "w") as file:
            json.dump(summary_stats, file, indent=4)
        print(f"[IO] Statistical summary saved to:   {json_path}")
        print("-" * 35)
        print("Session Complete. System shutdown cleanly.")
    except IOError as e:
         print(f"[Error] Failed to write JSON: {e}")

if __name__ == "__main__":
    main()