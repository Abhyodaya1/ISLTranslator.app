"""
Flask API Server for ISL Hand Sign Detection
Provides REST API endpoints for the React frontend
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from tensorflow import keras
import mediapipe as mp
from collections import deque

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
IMG_SIZE = 224
CONFIDENCE_THRESHOLD = 0.5
SMOOTHING_WINDOW = 15

class HandSignDetector:
    def __init__(self, model_path, labels_path):
        """Initialize detector with MediaPipe and TensorFlow model"""
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        
        # Load TensorFlow model with TF 2.20 compatibility
        try:
            import tensorflow as tf
            # Disable XLA for compatibility
            tf.config.optimizer.set_jit(False)
            
            self.model = keras.models.load_model(
                model_path,
                compile=False,
                safe_mode=False
            )
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'],
                run_eagerly=True  # Use eager execution for stability
            )
            print(f"✅ Model loaded successfully from {model_path}")
            print(f"   Input shape: {self.model.input_shape}")
            print(f"   Output classes: {self.model.output_shape[-1]}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("💡 Make sure the model was trained with train_simple.py")
            raise
        
        # Load labels
        try:
            with open(labels_path, 'r') as f:
                self.labels = [line.strip().split()[-1] for line in f if line.strip()]
            print(f"✅ Loaded {len(self.labels)} labels: {self.labels}")
        except Exception as e:
            print(f"❌ Error loading labels: {e}")
            self.labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
        
        # Prediction smoothing
        self.prediction_buffer = deque(maxlen=SMOOTHING_WINDOW)
        
    def extract_hand_region(self, frame, hand_landmarks):
        """Extract and preprocess hand region from frame"""
        h, w, _ = frame.shape
        
        # Get bounding box from landmarks
        x_coords = [lm.x for lm in hand_landmarks.landmark]
        y_coords = [lm.y for lm in hand_landmarks.landmark]
        
        x_min = int(min(x_coords) * w)
        y_min = int(min(y_coords) * h)
        x_max = int(max(x_coords) * w)
        y_max = int(max(y_coords) * h)
        
        # Add padding
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)
        
        # Extract region
        hand_region = frame[y_min:y_max, x_min:x_max]
        
        if hand_region.size == 0:
            return None
        
        # Resize maintaining aspect ratio on white background
        img_white = np.ones((IMG_SIZE, IMG_SIZE, 3), np.uint8) * 255
        
        region_h, region_w = hand_region.shape[:2]
        aspect_ratio = region_h / region_w
        
        if aspect_ratio > 1:
            new_h = IMG_SIZE
            new_w = int(IMG_SIZE / aspect_ratio)
        else:
            new_w = IMG_SIZE
            new_h = int(IMG_SIZE * aspect_ratio)
        
        # Resize hand region
        hand_resized = cv2.resize(hand_region, (new_w, new_h))
        
        # Center on white background
        y_offset = (IMG_SIZE - new_h) // 2
        x_offset = (IMG_SIZE - new_w) // 2
        img_white[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = hand_resized
        
        return img_white
    
    def predict(self, hand_image):
        """Make prediction on preprocessed hand image"""
        # Normalize image
        input_data = np.expand_dims(hand_image, axis=0).astype(np.float32) / 255.0
        
        # Get prediction
        prediction = self.model.predict(input_data, verbose=0)[0]
        
        # Add to buffer for smoothing
        self.prediction_buffer.append(prediction)
        
        # Average predictions over buffer
        avg_prediction = np.mean(self.prediction_buffer, axis=0)
        
        # Get best prediction
        index = np.argmax(avg_prediction)
        confidence = avg_prediction[index]
        
        return self.labels[index], confidence, avg_prediction.tolist()
    
    def process_image(self, image):
        """Process single image and return results"""
        # Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.hands.process(rgb_image)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract hand region
                hand_image = self.extract_hand_region(image, hand_landmarks)
                
                if hand_image is not None:
                    # Make prediction
                    label, confidence, all_predictions = self.predict(hand_image)
                    
                    # Only return if confidence is high enough
                    if confidence >= CONFIDENCE_THRESHOLD:
                        return {
                            'success': True,
                            'label': label,
                            'confidence': float(confidence),
                            'all_predictions': dict(zip(self.labels, all_predictions))
                        }
        
        return {
            'success': False,
            'error': 'No hand detected with sufficient confidence'
        }

# Initialize detector
detector = HandSignDetector("Model/keras_model.h5", "Model/labels.txt")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'labels': detector.labels
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict sign from image"""
    try:
        print("\n" + "="*60)
        print("📸 Received prediction request")
        
        # Get image from request
        data = request.json
        if 'image' not in data:
            print("❌ No image in request")
            return jsonify({'error': 'No image provided'}), 400
        
        print("✅ Image data received")
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1] if ',' in data['image'] else data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            print("❌ Failed to decode image")
            return jsonify({'error': 'Invalid image'}), 400
        
        print(f"✅ Image decoded: {image.shape}")
        
        # Process image and get prediction
        result = detector.process_image(image)
        
        if result['success']:
            print(f"🎯 PREDICTION: {result['label']} (Confidence: {result['confidence']:.2%})")
        else:
            print(f"⚠️ {result.get('error', 'No prediction')}")
        
        print("="*60)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("="*60)
        return jsonify({'error': str(e)}), 500

@app.route('/api/labels', methods=['GET'])
def get_labels():
    """Get all available labels"""
    return jsonify({
        'labels': detector.labels
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ISL Hand Sign Detection API Server")
    print("=" * 60)
    print(f"✅ Model loaded with {len(detector.labels)} signs")
    print(f"📋 Available signs: {', '.join(detector.labels)}")
    print(f"🌐 Starting server on http://localhost:5000")
    print("\n💡 Frontend Instructions:")
    print("   1. Open a new terminal")
    print("   2. cd frontend")
    print("   3. npm run dev")
    print("   4. Open http://localhost:5173")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
