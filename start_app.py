"""
Quick Start Script for ISL Translator Application
Starts the API server and provides frontend instructions
"""

import os
import sys
import subprocess
import time

def print_banner():
    print("=" * 70)
    print("🚀 ISHARA - ISL Translator Application Launcher")
    print("=" * 70)

def check_model_exists():
    """Check if model files exist"""
    model_path = "Model/keras_model.h5"
    labels_path = "Model/labels.txt"
    
    if not os.path.exists(model_path):
        print("❌ Model not found!")
        print("   Please train the model first using: python train_simple.py")
        return False
    
    if not os.path.exists(labels_path):
        print("❌ Labels file not found!")
        print("   Please train the model first using: python train_simple.py")
        return False
    
    print(f"✅ Model found: {model_path}")
    print(f"✅ Labels found: {labels_path}")
    return True

def check_frontend():
    """Check if frontend exists"""
    frontend_path = "frontend"
    if not os.path.exists(frontend_path):
        print("⚠️  Frontend folder not found at: frontend/")
        return False
    
    package_json = os.path.join(frontend_path, "package.json")
    if not os.path.exists(package_json):
        print("⚠️  package.json not found in frontend/")
        return False
    
    print(f"✅ Frontend found: {frontend_path}")
    return True

def main():
    print_banner()
    
    print("\n📋 Checking requirements...")
    
    # Check if model exists
    if not check_model_exists():
        sys.exit(1)
    
    # Check if frontend exists
    has_frontend = check_frontend()
    
    print("\n" + "=" * 70)
    print("🎯 Starting Application")
    print("=" * 70)
    
    print("\n1️⃣  Starting API Server...")
    print("   Server will start on: http://localhost:5000")
    print("   Press Ctrl+C to stop the server\n")
    
    if has_frontend:
        print("2️⃣  To start the frontend (in a NEW terminal):")
        print("   cd frontend")
        print("   npm install  (first time only)")
        print("   npm run dev")
        print("   Open: http://localhost:5173\n")
    
    print("=" * 70)
    print("\n⏳ Launching API server in 3 seconds...")
    time.sleep(3)
    
    # Start API server
    try:
        subprocess.run([sys.executable, "api_server.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        print("✅ API server stopped")

if __name__ == "__main__":
    main()
