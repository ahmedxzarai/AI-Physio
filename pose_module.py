# ---------------------------------------------------------------------------
# Project: AI-Physio | Real-Time Biomechanical Squat Analysis System
# File:    pose_module.py
# Author:  AHMED ZARAI
#
# Copyright (c) 2026 Ahmed Zarai. All rights reserved.
# ---------------------------------------------------------------------------

import math
import os
import sys
from typing import List, Tuple, Optional, Any

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PoseDetector:
    """
    Handles MediaPipe Pose Landmarker initialization, detection, and
    geometric calculations for biomechanical analysis.
    """
    def __init__(self, model_path: str = "pose_landmarker.task"):
        """
        Initializes the MediaPipe Pose Landmarker task.

        Args:
            model_path (str): Path to the .task model file.
        Raises:
            FileNotFoundError: If the model path is invalid.
        """
        if not os.path.exists(model_path):
            print(f"CRITICAL ERROR: Model file not found at: {model_path}")
            print("Please download 'pose_landmarker_heavy.task' and rename it.")
            sys.exit(1)

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            output_segmentation_masks=False,
            min_pose_detection_confidence=0.6,
            min_pose_presence_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)
        self.results: Optional[Any] = None
        print(f"[System] PoseDetector initialized successfully with model: {model_path}")

    def detect(self, frame: np.ndarray, timestamp_ms: int) -> Optional[Any]:
        """
        Performs asynchronous pose detection on a video frame.
        """
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame
        )
        self.results = self.detector.detect_for_video(mp_image, timestamp_ms)
        return self.results

    def get_landmarks(self, frame: np.ndarray) -> List[Tuple[int, int, int]]:
        """
        Extracts and denormalizes landmark coordinates to pixel space.

        Returns:
            List[Tuple[int, int, int]]: A list of (id, x, y) tuples.
        """
        landmark_list: List[Tuple[int, int, int]] = []

        if self.results and self.results.pose_landmarks:
            h, w, _ = frame.shape
            # We only detect one pose, so we access index [0]
            for idx, lm in enumerate(self.results.pose_landmarks[0]):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append((idx, cx, cy))

        return landmark_list

    @staticmethod
    def calculate_angle(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
        """
        Calculates the interior angle at vertex p2 defined by points p1, p2, p3
        using arctan2 for robust trigonometric calculation.

        Args:
            p1 (Tuple[float, float]): Start point (e.g., Hip)
            p2 (Tuple[float, float]): Vertex point (e.g., Knee)
            p3 (Tuple[float, float]): End point (e.g., Ankle)

        Returns:
            float: The angle in degrees (0-180).
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # Calculate the angle using atan2 to handle all quadrants correctly
        radians = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle = abs(math.degrees(radians))

        # Ensure the angle is the interior angle (always <= 180)
        if angle > 180.0:
            angle = 360.0 - angle

        return angle