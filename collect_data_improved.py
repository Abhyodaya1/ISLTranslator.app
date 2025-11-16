"""
Improved Data Collection Script for ISL Signs
Using MediaPipe Hands for accurate hand detection
"""

import cv2
import numpy as np
import os
import time
import mediapipe as mp

# Configuration
IMG_SIZE = 224  # Match training size
SAVE_FOLDER = "Data"

class DataCollector:
    def __init__(self, sign_name):
        """Initialize data collector for a specific sign"""
        self.sign_name = sign_name
        self.save_path = os.path.join(SAVE_FOLDER, sign_name)
        
        # Create directory if it doesn't exist
        os.makedirs(self.save_path, exist_ok=True)
        
        # Count existing images
        existing_images = [f for f in os.listdir(self.save_path) if f.endswith('.jpg')]
        self.counter = len(existing_images)
        print(f"📁 Saving to: {self.save_path}")
        print(f"📊 Existing images: {self.counter}")
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
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
            return None, None
        
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
        
        return img_white, (x_min, y_min, x_max, y_max)
    
    def collect(self):
        """Main collection loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        # Set camera resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print(f"\n✅ Camera opened! Collecting data for sign: {self.sign_name}")
        print("🎮 Controls:")
        print("   • Press 'S' or SPACE to save current hand image")
        print("   • Press 'Q' to quit")
        print("\n👋 Show your hand sign and press 'S' to save...\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Failed to read frame")
                break
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.hands.process(rgb_frame)
            
            output_frame = frame.copy()
            hand_image = None
            bbox = None
            
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
                    
                    if bbox:
                        x_min, y_min, x_max, y_max = bbox
                        cv2.rectangle(output_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # Add UI elements
            cv2.putText(output_frame, f"Collecting: {self.sign_name}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(output_frame, f"Images saved: {self.counter}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(output_frame, "Press 'S' to save | 'Q' to quit", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show frames
            cv2.imshow('Data Collection - Camera Feed', output_frame)
            
            if hand_image is not None:
                cv2.imshow('Hand Region (Will be saved)', hand_image)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s') or key == ord('S') or key == ord(' '):
                if hand_image is not None:
                    # Save image
                    timestamp = int(time.time() * 1000)
                    filename = f"{self.sign_name}_{timestamp}_{self.counter:04d}.jpg"
                    filepath = os.path.join(self.save_path, filename)
                    cv2.imwrite(filepath, hand_image)
                    self.counter += 1
                    print(f"✅ Saved: {filename} (Total: {self.counter})")
                else:
                    print("⚠️  No hand detected! Show your hand to the camera.")
            
            elif key == ord('q') or key == ord('Q'):
                print(f"\n👋 Stopping collection. Total images saved: {self.counter}")
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("✅ Collection complete!")


def main():
    """Main function to collect data"""
    print("=" * 60)
    print("📸 ISL Hand Sign Data Collection Tool")
    print("=" * 60)
    
    # Available signs
    available_signs = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
    
    print("\n📋 Available signs:")
    for i, sign in enumerate(available_signs, 1):
        print(f"   {i}. {sign}")
    
    print("\n💡 Or enter a custom sign name")
    
    # Get sign name from user
    sign_input = input("\n🎯 Enter sign name or number: ").strip()
    
    # Check if it's a number
    if sign_input.isdigit():
        index = int(sign_input) - 1
        if 0 <= index < len(available_signs):
            sign_name = available_signs[index]
        else:
            print("❌ Invalid number!")
            return
    elif sign_input:
        sign_name = sign_input
    else:
        print("❌ No sign name provided!")
        return
    
    # Start collection
    collector = DataCollector(sign_name)
    collector.collect()


if __name__ == "__main__":
    main()
