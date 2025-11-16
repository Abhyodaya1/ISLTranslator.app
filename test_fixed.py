import cv2
import numpy as np
import math
import pyttsx3
import mediapipe as mp
from tensorflow import keras

# initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 100)  # speed
engine.setProperty('volume', 1)
engine.startLoop(False)

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Load the trained model
try:
    model = keras.models.load_model("Model/keras_model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Read labels
labels = ["A", "B", "C", "Help", "Ok", "ThankYou", "Yes"]

cap = cv2.VideoCapture(0)
offset = 20
imgSize = 300
counter = 0
last_label = ""
cooldown = 30

def preprocess_hand_region(hand_region):
    """Preprocess hand region for model prediction"""
    # Resize to model input size
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    
    h, w = hand_region.shape[:2]
    aspectRatio = h / w
    
    if aspectRatio > 1:
        k = imgSize / h
        wCal = math.ceil(k * w)
        imgResize = cv2.resize(hand_region, (wCal, imgSize))
        wGap = math.ceil((imgSize - wCal) / 2)
        imgWhite[:, wGap:wCal + wGap] = imgResize
    else:
        k = imgSize / w
        hCal = math.ceil(k * h)
        imgResize = cv2.resize(hand_region, (imgSize, hCal))
        hGap = math.ceil((imgSize - hCal) / 2)
        imgWhite[hGap:hCal + hGap, :] = imgResize
    
    return imgWhite

print("Hand Sign Detection Started!")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        break
        
    frameOutput = frame.copy()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and find hands
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frameOutput, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get bounding box coordinates
            h, w, _ = frame.shape
            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * w)
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * h)
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * w)
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * h)
            
            # Add padding
            x_min = max(0, x_min - offset)
            y_min = max(0, y_min - offset)
            x_max = min(w, x_max + offset)
            y_max = min(h, y_max + offset)
            
            # Extract hand region
            hand_region = frame[y_min:y_max, x_min:x_max]
            
            if hand_region.size > 0:
                # Preprocess for model
                processed_hand = preprocess_hand_region(hand_region)
                
                # Make prediction
                try:
                    # Normalize the image
                    input_data = np.expand_dims(processed_hand, axis=0).astype(np.float32) / 255.0
                    prediction = model.predict(input_data, verbose=0)
                    index = np.argmax(prediction)
                    confidence = np.max(prediction)
                    
                    # Only show prediction if confidence is high enough
                    if confidence > 0.7:
                        current_label = labels[index]
                        
                        # Display prediction
                        cv2.putText(frameOutput, f"{current_label} ({confidence:.2f})", 
                                  (x_min, y_min - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.rectangle(frameOutput, (x_min, y_min), (x_max, y_max), (255, 0, 255), 2)
                        
                        # Text-to-speech
                        if (current_label != last_label) or (counter == 0):
                            engine.say(current_label)
                            last_label = current_label
                            counter = cooldown
                            
                        # Show processed hand image
                        cv2.imshow('Processed Hand', processed_hand)
                        
                except Exception as e:
                    print(f"Prediction error: {e}")
    
    if counter > 0:
        counter -= 1
    
    engine.iterate()
    cv2.imshow('Hand Sign Detection', frameOutput)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
engine.endLoop()
print("Application closed successfully!")