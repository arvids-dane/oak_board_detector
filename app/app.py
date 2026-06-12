import os
import sys
import base64
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.image_processor import ImageProcessor
from app.settings_manager import SettingsManager

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize processors
image_processor = ImageProcessor()
settings_manager = SettingsManager('../settings')

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

def frame_to_base64(frame):
    """Convert OpenCV frame to base64 string for sending over HTTP"""
    if frame is None:
        return None
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings"""
    return jsonify(settings_manager.get_all_settings())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings"""
    data = request.get_json()
    settings_manager.save_settings(data)
    return jsonify({"success": True, "settings": settings_manager.get_all_settings()})

@app.route('/api/settings/save', methods=['POST'])
def save_settings():
    """Save current settings to file"""
    data = request.get_json()
    success = settings_manager.save_settings(data)
    return jsonify({"success": success})

@app.route('/api/settings/load', methods=['GET'])
def load_settings():
    """Load settings from file"""
    settings = settings_manager.load_settings()
    return jsonify({"success": True, "settings": settings})

@app.route('/api/settings/reset', methods=['POST'])
def reset_settings():
    """Reset settings to defaults"""
    settings = settings_manager.reset_to_defaults()
    return jsonify({"success": True, "settings": settings})

@app.route('/api/camera/capture', methods=['POST'])
def capture_frame():
    """Capture frame from camera"""
    data = request.get_json() or {}
    source = data.get('source', '0')
    
    # Open camera if not already open
    if image_processor.cap is None:
        success, msg = image_processor.open_camera(source)
        if not success:
            return jsonify({"success": False, "error": msg}), 400
    
    # Capture frame
    success, result = image_processor.capture_frame()
    if not success:
        image_processor.close_camera()
        return jsonify({"success": False, "error": result}), 400
    
    frame_b64 = frame_to_base64(result)
    image_processor.close_camera()
    
    return jsonify({
        "success": True,
        "frame": frame_b64,
        "width": result.shape[1],
        "height": result.shape[0]
    })

@app.route('/api/image/upload', methods=['POST'])
def upload_image():
    """Upload image from file"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        
        success, result = image_processor.load_image_from_file(filepath)
        if not success:
            return jsonify({"success": False, "error": result}), 400
        
        frame_b64 = frame_to_base64(result)
        return jsonify({
            "success": True,
            "frame": frame_b64,
            "width": result.shape[1],
            "height": result.shape[0]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/process', methods=['POST'])
def process_frame():
    """Process current frame with settings"""
    settings = settings_manager.get_all_settings()
    
    success, result = image_processor.process_frame(settings)
    if not success:
        return jsonify({"success": False, "error": result}), 400
    
    roi_b64 = frame_to_base64(result["roi"])
    contours_b64 = frame_to_base64(result["contours_image"])
    
    return jsonify({
        "success": True,
        "roi": roi_b64,
        "contours": contours_b64,
        "contours_info": result["contours_info"]
    })

@app.route('/api/gcode/load', methods=['POST'])
def load_gcode():
    """Load G-code file"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files['file']
    try:
        filepath = os.path.join('../gcode', secure_filename(file.filename))
        Path('../gcode').mkdir(exist_ok=True)
        file.save(filepath)
        
        success, result = image_processor.load_gcode_file(filepath)
        if not success:
            return jsonify({"success": False, "error": result}), 400
        
        return jsonify({
            "success": True,
            "toolpath": result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/gcode/align', methods=['POST'])
def align_gcode():
    """Align G-code to detected board"""
    if image_processor.current_frame_with_contours is None:
        return jsonify({"success": False, "error": "No contours detected. Process frame first."}), 400
    
    # For now, we'll use dummy contour info
    # In real implementation, you'd extract this from process_frame
    contours_info = [{"area": 10000, "bbox": [50, 50, 200, 300]}]
    settings = settings_manager.get_all_settings()
    
    success, result = image_processor.align_toolpath_to_board(contours_info, settings)
    if not success:
        return jsonify({"success": False, "error": result}), 400
    
    return jsonify({
        "success": True,
        "alignment": result
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
