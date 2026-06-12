# Oak Board Detector

A comprehensive Python application for detecting oak board contours and aligning CNC toolpaths using real-time image analysis.

## Features

- **Live Camera Feed**: Capture frames from webcam or IP camera via RTSP
- **Image Loading**: Load images from file for offline analysis
- **Contour Detection**: Automatic oak board edge and contour detection using OpenCV
- **Image Processing**: 
  - Gaussian blur
  - Threshold adjustment
  - Brightness and contrast control
  - Lens distortion correction
  - Region of Interest (ROI) extraction
- **Calibration System**: Set pixel-to-millimeter conversion ratios
- **Settings Management**: Save, load, and reset processing parameters
- **G-Code Integration**: Load and preview G-code toolpaths
- **Toolpath Alignment**: Automatically align CNC toolpath to detected material position
- **Web-Based UI**: Modern, responsive browser interface optimized for 1920x1080 displays
- **Cross-Platform**: Works on Linux and Windows

## System Requirements

- Python 3.8 or higher
- Webcam or IP camera with RTSP support
- Modern web browser (Chrome, Firefox, Edge, Safari)
- 2GB RAM minimum
- Display resolution: 1920x1080 or higher recommended

## Installation

### Linux (Ubuntu/Debian/Fedora)

1. **Clone or extract the project:**
   ```bash
   cd oak_board_detector
   ```

2. **Make launcher executable:**
   ```bash
   chmod +x launch_linux.sh
   ```

3. **Run the launcher:**
   ```bash
   ./launch_linux.sh
   ```

The launcher will:
- Check for Python 3 installation
- Create a virtual environment
- Install all dependencies
- Start the application server

### Windows

1. **Extract the project folder**

2. **Double-click `launch_windows.bat`**

The launcher will:
- Check for Python installation
- Create a virtual environment
- Install all dependencies
- Start the application server

## Usage

### Starting the Application

**Linux:**
```bash
./launch_linux.sh
```

**Windows:**
```
Double-click launch_windows.bat
```

After startup, open your browser and navigate to:
```
http://localhost:5000
```

### Main Interface

The web interface is organized into four main panels:

#### Top Left: Live Camera Feed
- Displays the current image from camera or loaded file
- Shows image dimensions

#### Top Right: Controls and Sliders
**Image Input:**
- **Capture Frame**: Grab a single frame from connected camera
- **Load Image**: Select an image file from your computer

**Processing Controls:**
- **Process Frame**: Apply all settings and detect contours

**G-Code & Alignment:**
- **Load G-Code**: Load a .gcode or .ngc file for preview
- **Align Toolpath**: Automatically align loaded G-code to detected board position

**CV2 Parameters:**
- **Blur**: Gaussian blur kernel size (1-51, odd numbers)
- **Threshold 1**: Lower Canny edge detection threshold (0-255)
- **Threshold 2**: Upper Canny edge detection threshold (0-255)
- **Brightness**: Adjust image brightness (-100 to +100)
- **Contrast**: Adjust image contrast (0.5 to 3.0)
- **Distortion K1**: First lens distortion coefficient (-0.5 to 0.5)
- **Distortion K2**: Second lens distortion coefficient (-0.5 to 0.5)

**ROI Settings:**
- **ROI X/Y**: Starting position of region of interest
- **ROI Width/Height**: Size of region of interest

**Calibration:**
- **Object Width (mm)**: Physical width of calibration object in millimeters
- **Object Length (mm)**: Physical length of calibration object in millimeters
- **Object Width (px)**: Width of calibration object in pixels
- **Object Length (px)**: Length of calibration object in pixels

**Settings Management:**
- **Save Settings**: Store current parameters to settings file
- **Load Settings**: Restore previously saved parameters
- **Reset to Defaults**: Restore all parameters to default values

#### Middle Left: Region of Interest (ROI)
- Displays the extracted ROI based on current settings
- Updated after processing

#### Middle Right: Detected Board Contours
- Shows the processed image with detected oak board contours highlighted in green
- Displays contour statistics (count, area, bounding box)

### Keyboard Shortcuts

- **Ctrl+S** (Cmd+S on Mac): Save settings
- **Ctrl+L** (Cmd+L on Mac): Load settings
- **Ctrl+P** (Cmd+P on Mac): Process frame

## Configuration

### Settings File

Settings are automatically saved to:
- **Linux**: `settings/config.json`
- **Windows**: `settings\config.json`

### Camera Configuration

To use an IP camera with RTSP:

1. Note your RTSP URL (format: `rtsp://username:password@camera_ip:port/path`)
2. In the application, when capturing, the system will prompt for camera source
3. Enter your RTSP URL instead of "0"

Example RTSP URLs:
- Hikvision: `rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101`
- Reolink: `rtsp://admin:password@192.168.1.100:554/h264Preview_01_main`
- Dahua: `rtsp://admin:password@192.168.1.100:554/stream0`

## Troubleshooting

### Camera Not Working

**Linux:**
- Install camera libraries: `sudo apt-get install libopencv-dev`
- Check permissions: `ls -l /dev/video*`
- Grant permission: `sudo usermod -aG video $USER`

**Windows:**
- Update your webcam drivers
- Try using a different USB port
- Restart the application

### Python Not Found

**Linux:**
- Install Python 3: `sudo apt-get install python3 python3-pip`

**Windows:**
- Download Python from https://www.python.org/downloads/
- Make sure "Add Python to PATH" is checked during installation
- Restart your computer after installation

### Module Import Errors

Delete the virtual environment and rerun the launcher:

**Linux:**
```bash
rm -rf venv
./launch_linux.sh
```

**Windows:**
```cmd
rmdir /s venv
launch_windows.bat
```

### Port Already in Use

If port 5000 is already in use, modify the last line in `app/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to another port
```

## File Structure

```
oak_board_detector/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # Main Flask application
│   ├── image_processor.py       # OpenCV image processing
│   └── settings_manager.py      # Settings management
├── static/
│   ├── app.js                   # Frontend JavaScript
│   └── style.css                # Frontend CSS styling
├── templates/
│   └── index.html               # Main HTML template
├── settings/
│   └── config.json              # Saved settings (created on first run)
├── uploads/                     # Uploaded images directory
├── gcode/                        # G-code files directory
├── requirements.txt             # Python dependencies
├── launch_linux.sh              # Linux launcher script
├── launch_windows.bat           # Windows launcher script
├── .env.example                 # Environment variables example
└── README.md                    # This file
```

## API Reference

### Settings Endpoints

- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings in memory
- `POST /api/settings/save` - Save settings to file
- `GET /api/settings/load` - Load settings from file
- `POST /api/settings/reset` - Reset to default values

### Image Processing Endpoints

- `POST /api/camera/capture` - Capture frame from camera
- `POST /api/image/upload` - Upload and load image file
- `POST /api/process` - Process frame with current settings

### G-Code Endpoints

- `POST /api/gcode/load` - Load G-code file
- `POST /api/gcode/align` - Align toolpath to detected board

### Health Check

- `GET /api/health` - Server health status

## Performance Tips

1. **For live camera feed**: Use lower blur values for faster processing
2. **For better edge detection**: Adjust threshold values based on lighting conditions
3. **For accurate calibration**: Capture and measure a known-size object
4. **For large images**: Use ROI extraction to reduce processing area

## Known Limitations

1. Requires good lighting for accurate contour detection
2. Single board detection (processes largest contour as main board)
3. G-code preview is positional information only, not visual rendering
4. Distortion correction uses simple radial distortion model

## Future Enhancements

- Multi-board detection and tracking
- Real-time video processing with frame rate display
- Advanced distortion models (fisheye, perspective)
- G-code visualization overlay on detected contours
- Machine learning-based board detection
- Export results as PDF reports
- Video recording functionality

## License

This project is provided as-is for oak board detection and CNC alignment purposes.

## Support

For issues or feature requests, please check the documentation above or consult the source code comments.

## Credits

Built with:
- Flask - Web framework
- OpenCV - Image processing
- NumPy - Numerical computing
- Python 3 - Programming language
