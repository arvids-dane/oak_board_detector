# Oak Board Detector - Quick Start Guide

## 🚀 Quick Launch

### Linux
```bash
cd /home/user/oak_board_detector
./launch_linux.sh
```

### Windows
```
Navigate to: C:\path\to\oak_board_detector
Double-click: launch_windows.bat
```

## 🌐 Access the Application

Once the server starts, open your web browser and go to:
```
http://localhost:5000
```

## 📋 What to Do First

1. **Capture or Load an Image**
   - Click "📷 Capture Frame" for webcam capture
   - Or click "📁 Load Image" to select an image file

2. **Adjust Processing Parameters**
   - Use the sliders on the right panel to fine-tune:
     - Blur, Threshold, Brightness, Contrast
     - Distortion correction
     - ROI (Region of Interest) settings

3. **Process the Frame**
   - Click "⚙️ Process Frame" to detect board contours
   - Results appear in the ROI and Contours panels

4. **Calibrate (Optional)**
   - Set pixel-to-millimeter conversion for accurate measurements
   - Enter the physical dimensions of your calibration object

5. **Load G-Code (Optional)**
   - Click "📄 Load G-Code" to import a toolpath file
   - Click "🎯 Align Toolpath" to align it to the detected board

6. **Save Your Settings**
   - Click "💾 Save Settings" to store your configuration
   - Next time, click "📂 Load Settings" to restore it

## ⚙️ System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS
- **RAM**: 2GB minimum
- **Display**: 1920x1080 or higher recommended
- **Camera**: Webcam or IP camera with RTSP support

## 🔧 Troubleshooting

### Camera Not Detected?
- **Linux**: `sudo apt-get install libopencv-dev && sudo usermod -aG video $USER`
- **Windows**: Update webcam drivers or try a different USB port

### Python Not Found?
- **Linux**: `sudo apt-get install python3 python3-pip`
- **Windows**: Download from https://www.python.org/downloads/ (check "Add Python to PATH")

### Dependencies Missing?
- Delete the `venv` folder and rerun the launcher

### Port 5000 Already in Use?
- Edit `app/app.py`, change port from 5000 to another number (e.g., 5001)
- Restart the application

## 📁 Project Structure

```
oak_board_detector/
├── app/                 # Backend Flask application
│   ├── app.py          # Main server
│   ├── image_processor.py    # OpenCV processing
│   └── settings_manager.py   # Configuration management
├── templates/          # HTML files
├── static/             # CSS and JavaScript
├── settings/           # Saved configurations
├── uploads/            # User uploaded images
├── gcode/              # G-code files
├── launch_linux.sh     # Linux starter
├── launch_windows.bat  # Windows starter
├── requirements.txt    # Python dependencies
└── README.md          # Full documentation
```

## 🎯 Key Features

✅ Real-time camera capture & image loading
✅ Oak board contour detection with OpenCV
✅ 15+ adjustable image processing parameters
✅ Region of Interest (ROI) extraction
✅ Pixel-to-millimeter calibration
✅ G-code file loading and alignment
✅ Save/load/reset processing profiles
✅ Modern responsive web interface
✅ Cross-platform support (Windows, Linux, Mac)
✅ Optimized for 1920x1080 displays

## 🎮 Keyboard Shortcuts

- **Ctrl+S** - Save settings
- **Ctrl+L** - Load settings  
- **Ctrl+P** - Process frame

## 📞 Getting Help

Refer to the full README.md for detailed documentation and advanced usage.

---

**Status**: ✅ Ready to Use
**Version**: 1.0
**Last Updated**: 2026-06-10
