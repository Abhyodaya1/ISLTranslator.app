# 🚀 ISL Translator - Quick Start

## Current Status
✅ Model trained with **43,820 images** and **39 classes**
✅ API server updated for TensorFlow 2.20 compatibility
✅ Frontend ready to connect

## Start the Application

### Step 1: Start API Server (Terminal 1)

```bash
python api_server.py
```

Expected output:
```
🚀 ISL Hand Sign Detection API Server
✅ Model loaded with 39 signs
🌐 Starting server on http://localhost:5000
```

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install  # First time only
npm run dev
```

Open browser to: `http://localhost:5173`

### Step 3: Use the App

1. Click "Translate" in navigation
2. Allow camera permissions
3. Show hand signs
4. See predictions!

## Supported Signs (39 total)

- **Letters**: A-Z (26 signs)
- **Numbers**: 1-9 (9 signs)
- **Words**: Help, Ok, ThankYou, Yes (4 signs)

## Troubleshooting

**API won't start:**
```bash
pip install flask flask-cors opencv-python mediapipe tensorflow
```

**Frontend won't connect:**
- Check API is running on port 5000
- Allow camera permissions in browser
- Use Chrome browser (recommended)

**Low accuracy:**
- Use good lighting
- Plain background
- Hold hand steady
- Full hand visible

## Testing

Test detection with webcam:
```bash
python detect_improved.py
```

Test API health:
```bash
curl http://localhost:5000/api/health
```
