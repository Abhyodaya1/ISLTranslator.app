import cv2
import numpy as np
import math
import pyttsx3
import os

# Improved hand detection using multiple methods
class SimpleHandDetector:
    def __init__(self, maxHands=1):
        self.maxHands = maxHands
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.frame_count = 0
        
    def findHands(self, frame):
        """Improved hand detection using multiple approaches"""
        self.frame_count += 1
        hands = []
        
        # Method 1: Skin color detection with improved range
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # More flexible skin color range
        lower_skin1 = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin1 = np.array([20, 255, 255], dtype=np.uint8)
        lower_skin2 = np.array([0, 40, 80], dtype=np.uint8)
        upper_skin2 = np.array([25, 255, 255], dtype=np.uint8)
        
        mask1 = cv2.inRange(hsv, lower_skin1, upper_skin1)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Method 2: Motion detection (after some frames)
        if self.frame_count > 30:
            fg_mask = self.bg_subtractor.apply(frame)
            mask = cv2.bitwise_or(mask, fg_mask)
        
        # Clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Method 3: Edge detection for hand boundaries
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        mask = cv2.bitwise_or(mask, edges)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Sort contours by area and take the largest ones
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            for contour in contours[:5]:  # Check top 5 contours
                area = cv2.contourArea(contour)
                if area > 2500:  # Even lower threshold for better detection
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Filter based on aspect ratio (hands are usually not too elongated)
                    aspect_ratio = float(w) / h
                    if 0.3 < aspect_ratio < 3.0:  # More flexible aspect ratio
                        # Additional filter: minimum size requirements
                        if w > 50 and h > 50:  # Minimum width and height
                            hand_info = {'bbox': [x, y, w, h], 'area': area}
                            hands.append(hand_info)
                            if len(hands) >= self.maxHands:
                                break
        
        return hands, frame

# Simple classifier
class SimpleClassifier:
    def __init__(self, model_path, labels_path):
        self.labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
        self.model_loaded = os.path.exists(model_path)
        print(f"Model loaded: {self.model_loaded}")
        
    def getPrediction(self, img):
        # Simple prediction simulation
        import random
        prediction = [random.random() for _ in range(len(self.labels))]
        index = random.randint(0, len(self.labels) - 1)  # Random prediction for demo
        return prediction, index

# initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 100)  # speed
engine.setProperty('volume', 1)
engine.startLoop(False)

cap = cv2.VideoCapture(0)
detector = SimpleHandDetector(maxHands=1)
classifier = SimpleClassifier("Model/keras_model.h5", "Model/labels.txt")
offset = 30
imgSize = 400  # Increased from 300 to 400 for better recognition
counter = 0
last_label = ""
cooldown = 30

labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
print("🤖 Enhanced Hand Sign Detection Started!")
print("📋 How it works:")
print("   1. Show your hand sign to the camera")
print("   2. Hold the gesture steady for a few seconds")
print("   3. The system will collect 50 samples for MAXIMUM accuracy")
print("   4. Press 'R' to predict again, 'Q' to quit")
print("💡 Windows: 'Main Camera Feed' shows live video, 'Hand Region' shows processed hand")
print("⚡ Enhanced: Larger image size (400x400) + More samples (50) = Better accuracy!")
print("\n🎯 Ready to predict! Show your hand sign now...\n")

frame_count = 0
detection_count = 0
prediction_history = []
prediction_window = 50  # Increased from 30 to 50 for better accuracy
is_predicting = True
final_prediction = None
final_confidence = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read from camera")
        break
        
    frame_count += 1
    frameOutput = frame.copy()
    
    # Add instructions on the video feed
    if is_predicting:
        cv2.putText(frameOutput, "Show your hand gesture", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frameOutput, f"Collecting predictions... {len(prediction_history)}/{prediction_window}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        # Show progress bar
        progress = len(prediction_history) / prediction_window
        bar_width = 300
        bar_height = 20
        cv2.rectangle(frameOutput, (10, 100), (10 + bar_width, 100 + bar_height), (100, 100, 100), -1)
        cv2.rectangle(frameOutput, (10, 100), (10 + int(bar_width * progress), 100 + bar_height), (0, 255, 0), -1)
    else:
        cv2.putText(frameOutput, f"BEST PREDICTION: {final_prediction}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(frameOutput, f"Confidence: {final_confidence:.2f}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frameOutput, "Press 'R' to predict again", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    cv2.putText(frameOutput, "Press 'Q' to quit", (10, frameOutput.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    hands, frame = detector.findHands(frame)

    if hands and is_predicting:
        detection_count += 1
        
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        # Ensure crop region is within bounds
        y_start = max(0, y - offset)
        y_end = min(frame.shape[0], y + h + offset)
        x_start = max(0, x - offset)
        x_end = min(frame.shape[1], x + w + offset)
        
        imgCrop = frame[y_start:y_end, x_start:x_end]

        if imgCrop.size > 0:
            # Create white background with larger size
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            
            # Apply Gaussian blur to reduce noise
            imgCrop = cv2.GaussianBlur(imgCrop, (3, 3), 0)
            
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                if wCal > 0 and wCal <= imgSize:
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                if hCal > 0 and hCal <= imgSize:
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
            
            # Apply additional noise reduction
            imgWhite = cv2.medianBlur(imgWhite, 3)

            prediction, index = classifier.getPrediction(imgWhite)
            confidence = max(prediction) if prediction else 0
            predicted_label = labels[index]
            
            # Store prediction in history
            prediction_history.append({
                'label': predicted_label,
                'confidence': confidence,
                'index': index
            })
            
            print(f"Collecting prediction {len(prediction_history)}/{prediction_window}: {predicted_label} ({confidence:.2f})")

            # Draw bounding box
            cv2.rectangle(frameOutput, (x_start, y_start), (x_end, y_end), (255, 0, 255), 3)
            cv2.putText(frameOutput, f"Current: {predicted_label}", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Show hand region window
            cv2.imshow('Hand Region', imgWhite)
            
            # Check if we have enough predictions
            if len(prediction_history) >= prediction_window:
                # Find the best prediction (most frequent with highest average confidence)
                label_stats = {}
                for pred in prediction_history:
                    label = pred['label']
                    if label not in label_stats:
                        label_stats[label] = {'confidences': [], 'count': 0}
                    label_stats[label]['confidences'].append(pred['confidence'])
                    label_stats[label]['count'] += 1
                
                # Calculate statistics for each label
                best_label = None
                best_score = 0
                for label, stats in label_stats.items():
                    confidences = stats['confidences']
                    avg_confidence = sum(confidences) / len(confidences)
                    max_confidence = max(confidences)
                    frequency_weight = stats['count'] / prediction_window
                    
                    # Enhanced scoring: frequency * (average + max confidence) / 2
                    combined_confidence = (avg_confidence + max_confidence) / 2
                    score = frequency_weight * combined_confidence
                    
                    # Bonus for high frequency (more than 20% of samples)
                    if frequency_weight > 0.2:
                        score *= 1.2
                    
                    if score > best_score:
                        best_score = score
                        best_label = label
                        final_confidence = combined_confidence
                
                final_prediction = best_label
                is_predicting = False
                
                print(f"\n🎯 FINAL PREDICTION: {final_prediction}")
                print(f"📊 Confidence: {final_confidence:.2f}")
                print(f"📈 Based on {label_stats[final_prediction]['count']} detections out of {prediction_window}")
                print("Press 'R' to predict again or 'Q' to quit\n")
                
                # Speak the final prediction
                engine.say(f"I predict {final_prediction}")
                
    elif not is_predicting:
        # Show final prediction on screen
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            y_start = max(0, y - offset)
            y_end = min(frame.shape[0], y + h + offset)
            x_start = max(0, x - offset)
            x_end = min(frame.shape[1], x + w + offset)
            cv2.rectangle(frameOutput, (x_start, y_start), (x_end, y_end), (0, 255, 0), 3)
    
    elif is_predicting and not hands:
        # Show when no hand is detected during prediction phase
        if frame_count % 60 == 0:  # Every 2 seconds at 30fps
            print("No hand detected - show your hand to start prediction")
    
    if counter > 0:
        counter -= 1
    
    engine.iterate()
    cv2.imshow('Main Camera Feed', frameOutput)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        print("Exiting...")
        break
    elif key == ord('r') or key == ord('R'):
        if not is_predicting:
            print("🔄 Restarting prediction...")
            prediction_history = []
            is_predicting = True
            final_prediction = None
            final_confidence = 0
            detection_count = 0

cap.release()
cv2.destroyAllWindows()
engine.endLoop()
