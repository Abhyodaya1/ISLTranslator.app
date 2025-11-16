"""
Optimized ISL Hand Sign Detection System
Using MediaPipe Hands + TensorFlow Model
Features:
- MediaPipe for accurate hand tracking
- Real-time prediction with temporal smoothing
- Confidence-based filtering
- Visual feedback and voice output
"""

# Suppress TensorFlow warnings for cleaner output
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress INFO and WARNING
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN warnings
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

import cv2
import numpy as np
import math
import pyttsx3
from collections import deque
from tensorflow import keras
import mediapipe as mp

# Configuration
IMG_SIZE = 224  # Match training size
CONFIDENCE_THRESHOLD = 0.5  # Lower threshold for testing (was 0.7)
SMOOTHING_WINDOW = 15  # More frames for better stability
COOLDOWN_FRAMES = 30  # Frames between voice announcements

class HandSignDetector:
    def __init__(self, model_path, labels_path):
        """Initialize detector with MediaPipe and TensorFlow model"""
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Load TensorFlow model with custom objects for compatibility
        try:
            # Try loading with safe mode disabled for legacy models
            self.model = keras.models.load_model(
                model_path,
                compile=False,  # Don't compile, we'll do it manually
                safe_mode=False  # Allow loading legacy models
            )
            # Recompile the model
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            print(f"✅ Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("⚠️  Model has compatibility issues. Let me try alternative loading...")
            
            # Alternative: Try loading without custom objects
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(
                    model_path,
                    custom_objects=None,
                    compile=False,
                    safe_mode=False
                )
                self.model.compile(
                    optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy']
                )
                print(f"✅ Model loaded successfully (compatibility mode)")
            except Exception as e2:
                print(f"❌ Failed to load model: {e2}")
                print("\n💡 Solution: Please retrain the model using train_improved.py")
                print("   This will create a model compatible with TensorFlow 2.20")
                exit()
        
        # Load labels
        try:
            with open(labels_path, 'r') as f:
                self.labels = [line.strip().split()[-1] for line in f if line.strip()]
            print(f"✅ Loaded {len(self.labels)} labels: {self.labels}")
        except Exception as e:
            print(f"❌ Error loading labels: {e}")
            self.labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
            print(f"Using default labels: {self.labels}")
        
        # Prediction smoothing
        self.prediction_buffer = deque(maxlen=SMOOTHING_WINDOW)
        
        # Text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.engine.startLoop(False)
        
        # State tracking
        self.last_prediction = None
        self.cooldown_counter = 0
        
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
        
        # Add padding (20%)
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)
        
        # Extract region
        hand_region = frame[y_min:y_max, x_min:x_max]
        
        if hand_region.size == 0:
            return None, None
        
        # Resize maintaining aspect ratio on white background
        img_white = np.ones((IMG_SIZE, IMG_SIZE, 3), np.uint8) * 255
        
        region_h, region_w = hand_region.shape[:2]
        aspect_ratio = region_h / region_w
        
        if aspect_ratio > 1:
            # Height is larger
            new_h = IMG_SIZE
            new_w = int(IMG_SIZE / aspect_ratio)
        else:
            # Width is larger
            new_w = IMG_SIZE
            new_h = int(IMG_SIZE * aspect_ratio)
        
        # Resize hand region
        hand_resized = cv2.resize(hand_region, (new_w, new_h))
        
        # Center on white background
        y_offset = (IMG_SIZE - new_h) // 2
        x_offset = (IMG_SIZE - new_w) // 2
        img_white[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = hand_resized
        
        # Apply slight Gaussian blur to reduce noise
        img_white = cv2.GaussianBlur(img_white, (3, 3), 0)
        
        return img_white, (x_min, y_min, x_max, y_max)
    
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
        
        return self.labels[index], confidence, avg_prediction
    
    def process_frame(self, frame):
        """Process single frame and return results"""
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(rgb_frame)
        
        output_frame = frame.copy()
        hand_image = None
        prediction_info = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    output_frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
                
                # Extract hand region
                hand_image, bbox = self.extract_hand_region(frame, hand_landmarks)
                
                if hand_image is not None:
                    # Make prediction
                    label, confidence, all_predictions = self.predict(hand_image)
                    
                    # Only show if confidence is high enough
                    if confidence >= CONFIDENCE_THRESHOLD:
                        x_min, y_min, x_max, y_max = bbox
                        
                        # Draw bounding box
                        cv2.rectangle(output_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        
                        # Draw label with confidence
                        label_text = f"{label} ({confidence:.2f})"
                        cv2.putText(output_frame, label_text, (x_min, y_min - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        prediction_info = {
                            'label': label,
                            'confidence': confidence,
                            'all_predictions': all_predictions
                        }
                        
                        # Text-to-speech with cooldown
                        if self.cooldown_counter == 0:
                            if label != self.last_prediction:
                                self.engine.say(label)
                                self.last_prediction = label
                                self.cooldown_counter = COOLDOWN_FRAMES
                        
        # Update cooldown
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
        
        # Iterate TTS engine
        self.engine.iterate()
        
        return output_frame, hand_image, prediction_info
    
    def cleanup(self):
        """Cleanup resources"""
        self.hands.close()
        self.engine.endLoop()


def main():
    """Main application loop"""
    print("=" * 60)
    print("🤖 ISL Hand Sign Detection System - MediaPipe Edition")
    print("=" * 60)
    print("✨ Features:")
    print("   • MediaPipe Hands for accurate tracking")
    print("   • Real-time prediction with smoothing")
    print("   • Confidence-based filtering")
    print("   • Voice feedback")
    print("\n🎮 Controls:")
    print("   • Press 'Q' to quit")
    print("   • Press 'S' to toggle statistics")
    print("=" * 60)
    
    # Initialize detector
    detector = HandSignDetector("Model/keras_model.h5", "Model/labels.txt")
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    show_stats = False
    frame_count = 0
    
    print("\n✅ Camera opened successfully!")
    print("👋 Show your hand sign to the camera...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Failed to read frame")
            break
        
        frame_count += 1
        
        # Process frame
        output_frame, hand_image, prediction_info = detector.process_frame(frame)
        
        # Add instructions
        cv2.putText(output_frame, "Press 'Q' to quit | 'S' for stats", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show statistics if enabled
        if show_stats and prediction_info:
            y_pos = 70
            cv2.putText(output_frame, "Predictions:", (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            y_pos += 30
            
            for i, (label, prob) in enumerate(zip(detector.labels, prediction_info['all_predictions'])):
                text = f"{label}: {prob:.3f}"
                color = (0, 255, 0) if prob >= CONFIDENCE_THRESHOLD else (150, 150, 150)
                cv2.putText(output_frame, text, (10, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                y_pos += 25
        
        # Show frames
        cv2.imshow('ISL Hand Sign Detection', output_frame)
        
        if hand_image is not None:
            cv2.imshow('Hand Region (Processed)', hand_image)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\n👋 Exiting...")
            break
        elif key == ord('s') or key == ord('S'):
            show_stats = not show_stats
            print(f"📊 Statistics: {'ON' if show_stats else 'OFF'}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    detector.cleanup()
    print("✅ Application closed successfully!")


if __name__ == "__main__":
    main()
