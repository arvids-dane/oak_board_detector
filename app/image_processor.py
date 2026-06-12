import cv2
import numpy as np
from pathlib import Path

class ImageProcessor:
    def __init__(self):
        self.cap = None
        self.current_frame = None
        self.current_frame_roi = None
        self.current_frame_with_contours = None

    def open_camera(self, source="0"):
        """Open camera source (0 for webcam, or RTSP URL)"""
        try:
            if source == "0" or source == 0:
                self.cap = cv2.VideoCapture(0)
            else:
                # RTSP URL
                self.cap = cv2.VideoCapture(source)
            
            if not self.cap.isOpened():
                return False, "Failed to open camera"
            return True, "Camera opened successfully"
        except Exception as e:
            return False, str(e)

    def close_camera(self):
        """Close camera if open"""
        if self.cap:
            self.cap.release()
            self.cap = None

    def capture_frame(self):
        """Capture single frame from camera"""
        if self.cap is None:
            return False, "Camera not initialized"
        
        try:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                return True, frame
            return False, "Failed to capture frame"
        except Exception as e:
            return False, str(e)

    def load_image_from_file(self, file_path):
        """Load image from file"""
        try:
            if not Path(file_path).exists():
                return False, "File not found"
            
            frame = cv2.imread(str(file_path))
            if frame is None:
                return False, "Failed to load image"
            
            self.current_frame = frame
            return True, frame
        except Exception as e:
            return False, str(e)

    def apply_preprocessing(self, frame, settings):
        """Apply blur, brightness, contrast adjustments"""
        # Blur
        blur_value = int(settings.get("blur", 5))
        if blur_value > 0 and blur_value % 2 == 1:
            frame = cv2.GaussianBlur(frame, (blur_value, blur_value), 0)

        # Brightness and Contrast
        brightness = float(settings.get("brightness", 0))
        contrast = float(settings.get("contrast", 1.0))
        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

        # Distortion correction (simple)
        k1 = float(settings.get("distortion_k1", 0.0))
        k2 = float(settings.get("distortion_k2", 0.0))
        if k1 != 0 or k2 != 0:
            h, w = frame.shape[:2]
            camera_matrix = np.array([
                [w, 0, w/2],
                [0, w, h/2],
                [0, 0, 1]
            ], dtype=np.float32)
            dist_coeffs = np.array([k1, k2, 0, 0], dtype=np.float32)
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

        return frame

    def extract_roi(self, frame, settings):
        """Extract Region of Interest"""
        roi_x = int(settings.get("roi_x", 0))
        roi_y = int(settings.get("roi_y", 0))
        roi_width = int(settings.get("roi_width", 640))
        roi_height = int(settings.get("roi_height", 480))

        h, w = frame.shape[:2]
        
        # Ensure ROI is within bounds
        x1 = max(0, min(roi_x, w - 1))
        y1 = max(0, min(roi_y, h - 1))
        x2 = min(w, x1 + roi_width)
        y2 = min(h, y1 + roi_height)

        roi = frame[y1:y2, x1:x2]
        self.current_frame_roi = roi
        return roi

    def detect_board_contours(self, frame, settings):
        """Detect oak board contours using Canny edge detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        threshold1 = int(settings.get("threshold1", 100))
        threshold2 = int(settings.get("threshold2", 200))
        
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours by area
        min_area = float(settings.get("contour_min_area", 1000))
        filtered_contours = [c for c in contours if cv2.contourArea(c) > min_area]

        # Draw contours on frame
        frame_with_contours = frame.copy()
        cv2.drawContours(frame_with_contours, filtered_contours, -1, (0, 255, 0), 2)

        self.current_frame_with_contours = frame_with_contours

        # Extract contour information
        contour_info = []
        for cnt in filtered_contours:
            area = cv2.contourArea(cnt)
            rect = cv2.boundingRect(cnt)
            contour_info.append({
                "area": area,
                "bbox": list(rect),
                "contour": cnt.tolist()
            })

        return frame_with_contours, contour_info

    def process_frame(self, settings):
        """Full processing pipeline"""
        if self.current_frame is None:
            return False, "No frame loaded"

        try:
            # Apply preprocessing
            processed = self.apply_preprocessing(self.current_frame.copy(), settings)

            # Extract ROI
            roi = self.extract_roi(processed, settings)

            # Detect board contours
            frame_with_contours, contours_info = self.detect_board_contours(roi, settings)

            return True, {
                "roi": self.current_frame_roi,
                "contours_image": frame_with_contours,
                "contours_info": contours_info
            }
        except Exception as e:
            return False, str(e)

    def load_gcode_file(self, file_path):
        """Load and parse G-code file"""
        try:
            with open(file_path, 'r') as f:
                gcode_lines = f.readlines()
            
            toolpath = []
            for line in gcode_lines:
                line = line.strip()
                if line.startswith('G') or line.startswith('X') or line.startswith('Y'):
                    toolpath.append(line)
            
            return True, toolpath
        except Exception as e:
            return False, str(e)

    def align_toolpath_to_board(self, contours_info, calibration_settings):
        """Align G-code toolpath to detected board position"""
        if not contours_info:
            return False, "No contours detected"

        try:
            # Use largest contour as board
            largest_contour = max(contours_info, key=lambda x: x["area"])
            bbox = largest_contour["bbox"]
            board_x, board_y, board_w, board_h = bbox

            # Get calibration data
            px_to_mm_x = float(calibration_settings.get("calibrated_object_width_mm", 100)) / float(calibration_settings.get("calibrated_object_width_px", 50))
            px_to_mm_y = float(calibration_settings.get("calibrated_object_length_mm", 200)) / float(calibration_settings.get("calibrated_object_length_px", 100))

            # Calculate offset
            offset_x_mm = board_x * px_to_mm_x
            offset_y_mm = board_y * px_to_mm_y

            alignment_info = {
                "board_position_px": {"x": board_x, "y": board_y},
                "board_size_px": {"width": board_w, "height": board_h},
                "offset_mm": {"x": offset_x_mm, "y": offset_y_mm},
                "calibration": {
                    "px_to_mm_x": px_to_mm_x,
                    "px_to_mm_y": px_to_mm_y
                }
            }

            return True, alignment_info
        except Exception as e:
            return False, str(e)
