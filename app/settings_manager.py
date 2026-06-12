import json
import os
from pathlib import Path

class SettingsManager:
    def __init__(self, settings_dir="settings"):
        self.settings_dir = Path(settings_dir)
        self.settings_dir.mkdir(exist_ok=True)
        self.settings_file = self.settings_dir / "config.json"
        self.default_settings = {
            "blur": 5,
            "threshold1": 100,
            "threshold2": 200,
            "brightness": 0,
            "contrast": 1.0,
            "distortion_k1": 0.0,
            "distortion_k2": 0.0,
            "roi_x": 0,
            "roi_y": 0,
            "roi_width": 640,
            "roi_height": 480,
            "calibrated_object_width_mm": 100.0,
            "calibrated_object_length_mm": 200.0,
            "calibrated_object_width_px": 50,
            "calibrated_object_length_px": 100,
            "camera_source": "0",  # 0 for webcam, or RTSP URL
            "contour_min_area": 1000
        }
        self.current_settings = self.load_settings()

    def load_settings(self):
        """Load settings from file or return defaults"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.default_settings, **settings}
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.default_settings.copy()
        return self.default_settings.copy()

    def save_settings(self, settings_dict):
        """Save settings to file"""
        try:
            self.current_settings = {**self.default_settings, **settings_dict}
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.current_settings = self.default_settings.copy()
        self.save_settings(self.current_settings)
        return self.current_settings

    def get_setting(self, key):
        """Get a single setting value"""
        return self.current_settings.get(key, self.default_settings.get(key))

    def set_setting(self, key, value):
        """Set a single setting value"""
        self.current_settings[key] = value

    def get_all_settings(self):
        """Get all current settings"""
        return self.current_settings.copy()
