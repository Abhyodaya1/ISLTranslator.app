"""
Quick Model Test - Verify model loads and can make predictions
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import warnings
warnings.filterwarnings('ignore')

import numpy as np
from tensorflow import keras

print("=" * 60)
print("🧪 ISL Model Test")
print("=" * 60)

# Load model
print("\n📦 Loading model...")
try:
    model = keras.models.load_model("Model/keras_model.h5", compile=False, safe_mode=False)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit(1)

# Load labels
with open("Model/labels.txt", "r") as f:
    labels = [line.strip().split()[-1] for line in f if line.strip()]
print(f"✅ Loaded {len(labels)} labels: {labels}")

# Test prediction with dummy data
print("\n🧪 Testing prediction with random image...")
dummy_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
prediction = model.predict(dummy_image, verbose=0)

print(f"✅ Prediction shape: {prediction.shape}")
print(f"✅ Predicted class: {labels[np.argmax(prediction)]}")
print(f"✅ Confidence: {np.max(prediction):.4f}")

print("\n" + "=" * 60)
print("🎉 Model is working correctly!")
print("=" * 60)
print("\n💡 You can now run: python detect_improved.py")
print("   to use the full detection system with camera.")
