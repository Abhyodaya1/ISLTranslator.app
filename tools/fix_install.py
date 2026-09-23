#!/usr/bin/env python
"""
Fix broken PostgreSQL SSL certificate and install TensorFlow
"""
import os
import subprocess
import sys

print("=" * 70)
print("FIXING SSL CERTIFICATE AND INSTALLING TENSORFLOW")
print("=" * 70)

# Remove broken PostgreSQL certificate references
env = os.environ.copy()
if 'CURL_CA_BUNDLE' in env:
    print("[*] Removing broken CURL_CA_BUNDLE...")
    del env['CURL_CA_BUNDLE']

if 'SSL_CERT_FILE' in env:
    print("[*] Removing broken SSL_CERT_FILE...")
    del env['SSL_CERT_FILE']

print("\n[*] Installing TensorFlow (this may take 5-10 minutes)...")
print("-" * 70)

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "tensorflow", "--no-cache-dir"],
    env=env
)

print("-" * 70)

if result.returncode == 0:
    print("\n[SUCCESS] TensorFlow installed successfully!")

    # Verify installation
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        print(f"TensorFlow Version: {tf.__version__}")
        print(f"GPUs Found: {len(gpus)}")
        if gpus:
            for gpu in gpus:
                print(f"  - {gpu.name}")
        else:
            print("No GPU detected - will use CPU for training")
        print("\n[READY] You can now run: python FINAL_RUN.py")
    except Exception as e:
        print(f"[ERROR] Could not verify: {e}")
else:
    print(f"\n[FAILED] Installation failed with exit code {result.returncode}")
    sys.exit(1)
