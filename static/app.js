// Global state
let currentSettings = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Oak Board Detector...');
    loadSettings();
    setupEventListeners();
});

// Setup all event listeners
function setupEventListeners() {
    // Image input buttons
    document.getElementById('captureBtn').addEventListener('click', captureFrame);
    document.getElementById('loadImageBtn').addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);

    // G-Code buttons
    document.getElementById('loadGcodeBtn').addEventListener('click', () => {
        document.getElementById('gcodeInput').click();
    });
    document.getElementById('gcodeInput').addEventListener('change', handleGcodeSelect);
    document.getElementById('alignToolpathBtn').addEventListener('click', alignToolpath);

    // Process button
    document.getElementById('processBtn').addEventListener('click', processFrame);

    // Slider listeners
    const sliders = {
        'blurSlider': 'blur',
        'threshold1Slider': 'threshold1',
        'threshold2Slider': 'threshold2',
        'brightnessSlider': 'brightness',
        'contrastSlider': 'contrast',
        'distortionK1Slider': 'distortion_k1',
        'distortionK2Slider': 'distortion_k2',
        'roiXSlider': 'roi_x',
        'roiYSlider': 'roi_y',
        'roiWidthSlider': 'roi_width',
        'roiHeightSlider': 'roi_height'
    };

    Object.keys(sliders).forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const settingKey = sliders[sliderId];
        const valueSpan = document.getElementById(sliderId.replace('Slider', 'Value'));
        
        slider.addEventListener('input', function() {
            let value = parseFloat(this.value);
            currentSettings[settingKey] = value;
            if (valueSpan) valueSpan.textContent = value;
        });
    });

    // Calibration inputs
    document.getElementById('calibWidthMm').addEventListener('change', function() {
        currentSettings.calibrated_object_width_mm = parseFloat(this.value);
    });
    document.getElementById('calibLengthMm').addEventListener('change', function() {
        currentSettings.calibrated_object_length_mm = parseFloat(this.value);
    });
    document.getElementById('calibWidthPx').addEventListener('change', function() {
        currentSettings.calibrated_object_width_px = parseInt(this.value);
    });
    document.getElementById('calibLengthPx').addEventListener('change', function() {
        currentSettings.calibrated_object_length_px = parseInt(this.value);
    });

    // Settings management
    document.getElementById('saveSettingsBtn').addEventListener('click', saveSettings);
    document.getElementById('loadSettingsBtn').addEventListener('click', loadSettingsFromFile);
    document.getElementById('resetSettingsBtn').addEventListener('click', resetSettings);
}

// Load settings from server
async function loadSettings() {
    try {
        const response = await fetch('/api/settings');
        const settings = await response.json();
        currentSettings = settings;
        updateUIWithSettings(settings);
        showStatus('Settings loaded', 'success');
    } catch (error) {
        console.error('Error loading settings:', error);
        showStatus('Error loading settings', 'error');
    }
}

// Update UI with settings values
function updateUIWithSettings(settings) {
    // Update sliders
    const sliderMappings = {
        'blurSlider': 'blur',
        'threshold1Slider': 'threshold1',
        'threshold2Slider': 'threshold2',
        'brightnessSlider': 'brightness',
        'contrastSlider': 'contrast',
        'distortionK1Slider': 'distortion_k1',
        'distortionK2Slider': 'distortion_k2',
        'roiXSlider': 'roi_x',
        'roiYSlider': 'roi_y',
        'roiWidthSlider': 'roi_width',
        'roiHeightSlider': 'roi_height'
    };

    Object.keys(sliderMappings).forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const settingKey = sliderMappings[sliderId];
        const valueSpan = document.getElementById(sliderId.replace('Slider', 'Value'));
        
        if (settings[settingKey] !== undefined) {
            slider.value = settings[settingKey];
            if (valueSpan) valueSpan.textContent = settings[settingKey];
        }
    });

    // Update calibration inputs
    document.getElementById('calibWidthMm').value = settings.calibrated_object_width_mm || 100;
    document.getElementById('calibLengthMm').value = settings.calibrated_object_length_mm || 200;
    document.getElementById('calibWidthPx').value = settings.calibrated_object_width_px || 50;
    document.getElementById('calibLengthPx').value = settings.calibrated_object_length_px || 100;
}

// Capture frame from camera
async function captureFrame() {
    showStatus('Capturing frame from camera...', '');
    try {
        const response = await fetch('/api/camera/capture', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source: '0' })
        });

        if (!response.ok) throw new Error('Capture failed');
        
        const data = await response.json();
        if (data.success) {
            displayImage('cameraFeed', data.frame);
            document.getElementById('imageSizeInfo').textContent = `${data.width}x${data.height}px`;
            showStatus('Frame captured successfully', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Capture error:', error);
        showStatus('Error capturing frame', 'error');
    }
}

// Handle file selection for image
async function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    showStatus('Uploading image...', '');
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/image/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            displayImage('cameraFeed', data.frame);
            document.getElementById('imageSizeInfo').textContent = `${data.width}x${data.height}px`;
            showStatus('Image loaded successfully', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showStatus('Error uploading image', 'error');
    }

    // Reset file input
    event.target.value = '';
}

// Handle G-code file selection
async function handleGcodeSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    showStatus('Loading G-code file...', '');
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/gcode/load', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            console.log('G-code loaded:', data.toolpath.length, 'lines');
            showStatus(`G-code loaded: ${data.toolpath.length} commands`, 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('G-code load error:', error);
        showStatus('Error loading G-code', 'error');
    }

    event.target.value = '';
}

// Process frame with current settings
async function processFrame() {
    showStatus('Processing frame...', '');
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentSettings)
        });

        if (!response.ok) throw new Error('Processing failed');
        
        const data = await response.json();
        if (data.success) {
            displayImage('roiImage', data.roi);
            displayImage('contoursImage', data.contours);
            
            // Display contour information
            const contoursInfo = data.contours_info;
            let infoHtml = `<strong>Detected ${contoursInfo.length} contours:</strong><br>`;
            contoursInfo.forEach((contour, idx) => {
                infoHtml += `Contour ${idx + 1}: Area=${contour.area.toFixed(0)}px², BBox=${contour.bbox.join(', ')}<br>`;
            });
            document.getElementById('contoursInfo').innerHTML = infoHtml;
            
            showStatus('Frame processed successfully', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Processing error:', error);
        showStatus('Error processing frame', 'error');
    }
}

// Align toolpath to board
async function alignToolpath() {
    showStatus('Aligning toolpath...', '');
    try {
        const response = await fetch('/api/gcode/align', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (data.success) {
            const alignment = data.alignment;
            let message = `Toolpath aligned!<br>`;
            message += `Board position: (${alignment.board_position_px.x}, ${alignment.board_position_px.y})px<br>`;
            message += `Offset: (${alignment.offset_mm.x.toFixed(2)}, ${alignment.offset_mm.y.toFixed(2)})mm`;
            document.getElementById('contoursInfo').innerHTML = `<strong>${message}</strong>`;
            
            showStatus('Toolpath aligned successfully', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Alignment error:', error);
        showStatus('Error aligning toolpath', 'error');
    }
}

// Save settings to server
async function saveSettings() {
    showStatus('Saving settings...', '');
    try {
        const response = await fetch('/api/settings/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentSettings)
        });

        const data = await response.json();
        if (data.success) {
            showStatus('Settings saved successfully', 'success');
        } else {
            showStatus('Error saving settings', 'error');
        }
    } catch (error) {
        console.error('Save error:', error);
        showStatus('Error saving settings', 'error');
    }
}

// Load settings from file
async function loadSettingsFromFile() {
    showStatus('Loading settings...', '');
    try {
        const response = await fetch('/api/settings/load');
        const data = await response.json();
        
        if (data.success) {
            currentSettings = data.settings;
            updateUIWithSettings(data.settings);
            showStatus('Settings loaded from file', 'success');
        } else {
            showStatus('Error loading settings', 'error');
        }
    } catch (error) {
        console.error('Load error:', error);
        showStatus('Error loading settings', 'error');
    }
}

// Reset settings to defaults
async function resetSettings() {
    if (!confirm('Reset all settings to default values?')) return;
    
    showStatus('Resetting settings...', '');
    try {
        const response = await fetch('/api/settings/reset', {
            method: 'POST'
        });

        const data = await response.json();
        if (data.success) {
            currentSettings = data.settings;
            updateUIWithSettings(data.settings);
            showStatus('Settings reset to defaults', 'success');
        } else {
            showStatus('Error resetting settings', 'error');
        }
    } catch (error) {
        console.error('Reset error:', error);
        showStatus('Error resetting settings', 'error');
    }
}

// Display image in specified element
function displayImage(elementId, base64Data) {
    const img = document.getElementById(elementId);
    img.src = `data:image/jpeg;base64,${base64Data}`;
}

// Show status message
function showStatus(message, type) {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = 'status-info';
    if (type) {
        statusEl.classList.add(type);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 's':
                e.preventDefault();
                saveSettings();
                break;
            case 'l':
                e.preventDefault();
                loadSettingsFromFile();
                break;
            case 'p':
                e.preventDefault();
                processFrame();
                break;
        }
    }
});
