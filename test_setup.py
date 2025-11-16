"""
Quick Test Script to Verify Setup
Tests all components without running the full application
"""

import sys
import importlib

def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("🔍 Testing Package Imports")
    print("=" * 60)
    
    packages = {
        'cv2': 'opencv-python',
        'tensorflow': 'tensorflow',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'pyttsx3': 'pyttsx3',
        'matplotlib': 'matplotlib (optional for training)'
    }
    
    all_good = True
    for package, name in packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {name}: OK")
        except ImportError:
            print(f"❌ {name}: MISSING")
            all_good = False
    
    return all_good

def test_model_files():
    """Check if model files exist"""
    print("\n" + "=" * 60)
    print("📁 Checking Model Files")
    print("=" * 60)
    
    import os
    
    files_to_check = {
        'Model/keras_model.h5': 'Trained model',
        'Model/labels.txt': 'Class labels'
    }
    
    all_exist = True
    for filepath, description in files_to_check.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {description}: {filepath} ({size:,} bytes)")
        else:
            print(f"⚠️  {description}: {filepath} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_camera():
    """Test camera access"""
    print("\n" + "=" * 60)
    print("📷 Testing Camera Access")
    print("=" * 60)
    
    import cv2
    
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            print(f"✅ Camera working: {w}x{h} resolution")
            cap.release()
            return True
        else:
            print("❌ Camera opened but cannot read frames")
            cap.release()
            return False
    else:
        print("❌ Cannot open camera")
        return False

def test_mediapipe():
    """Test MediaPipe hands"""
    print("\n" + "=" * 60)
    print("🖐️ Testing MediaPipe Hands")
    print("=" * 60)
    
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        hands.close()
        print("✅ MediaPipe Hands: OK")
        return True
    except Exception as e:
        print(f"❌ MediaPipe Hands: FAILED - {e}")
        return False

def test_tensorflow():
    """Test TensorFlow"""
    print("\n" + "=" * 60)
    print("🧠 Testing TensorFlow")
    print("=" * 60)
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        
        # Check if GPU is available
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU detected: {len(gpus)} device(s)")
        else:
            print("ℹ️  No GPU detected (CPU mode)")
        
        return True
    except Exception as e:
        print(f"❌ TensorFlow: FAILED - {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🔧 ISL Hand Sign Detection - System Test")
    print("=" * 60)
    
    results = {
        'Imports': test_imports(),
        'Model Files': test_model_files(),
        'Camera': test_camera(),
        'MediaPipe': test_mediapipe(),
        'TensorFlow': test_tensorflow()
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! System is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Run: python detect_improved.py")
        print("   2. Or collect data: python collect_data_improved.py")
        print("   3. Or train model: python train_improved.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        
        if not results['Model Files']:
            print("\n💡 To create model files:")
            print("   python train_improved.py")
        
        if not results['Camera']:
            print("\n💡 Camera issues:")
            print("   - Close other apps using the camera")
            print("   - Check camera permissions")
            print("   - Try different camera index in code")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
