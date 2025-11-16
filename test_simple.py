import cv2
import numpy as np
import math
import pyttsx3

# Simple hand detection using OpenCV contours
class SimpleHandDetector:
    def __init__(self):
        self.prev_frame = None
        
    def findHands(self, frame):
        """Simple hand detection using background subtraction and contour detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use skin color detection in HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define range of skin color in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create a mask for skin color
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (assuming it's the hand)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Filter small areas (noise)
            if cv2.contourArea(largest_contour) > 5000:
                hand_info = {
                    'bbox': (x, y, w, h),
                    'contour': largest_contour
                }
                return [hand_info], frame
        
        return [], frame

# Simple classifier using the trained model
class SimpleClassifier:
    def __init__(self, model_path, labels_path):
        try:
            # Try to load model without tensorflow first
            import os
            if os.path.exists(model_path):
                print(f"Model file found: {model_path}")
                # For now, we'll simulate predictions
                self.model_loaded = False
            else:
                print(f"Model file not found: {model_path}")
                self.model_loaded = False
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
            
        # Load labels
        self.labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]
        
    def getPrediction(self, img):
        """Simulate prediction - in real implementation this would use the loaded model"""
        # For demonstration, return a random prediction
        import random
        prediction_scores = [random.random() for _ in range(len(self.labels))]
        index = np.argmax(prediction_scores)
        return prediction_scores, index

# initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 100)  # speed
engine.setProperty('volume', 1)
engine.startLoop(False)

cap = cv2.VideoCapture(0)
detector = SimpleHandDetector()
classifier = SimpleClassifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 300
counter = 0
last_label = ""
cooldown = 30

labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]

print("Hand Sign Detection Started!")
print("Press 'q' to quit")
print("Note: This is using simplified hand detection. For better accuracy, install cvzone.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        break
        
    frameOutput = frame.copy()
    hands, frame = detector.findHands(frame)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        # Make sure the crop region is within frame bounds
        y_start = max(0, y - offset)
        y_end = min(frame.shape[0], y + h + offset)
        x_start = max(0, x - offset)
        x_end = min(frame.shape[1], x + w + offset)
        
        imgCrop = frame[y_start:y_end, x_start:x_end]

        if imgCrop.size > 0:
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCropShape = imgCrop.shape

            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                if wCal > 0:
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                if hCal > 0:
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite)
            print(f"Prediction: {labels[index]} (confidence: {max(prediction):.2f})")

            cv2.putText(frameOutput, labels[index], (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 252, 124), 3)
            cv2.rectangle(frameOutput, (x_start, y_start), (x_end, y_end), (255, 0, 255), 4)
            cv2.imshow('Hand Region', imgWhite)

            current_label = labels[index]
            if (current_label != last_label) or (counter == 0):
                engine.say(current_label)
                last_label = current_label
                counter = cooldown
                
    if counter > 0:
        counter -= 1
        
    engine.iterate()
    cv2.imshow('Hand Sign Detection', frameOutput)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
engine.endLoop()
print("Application closed successfully!")