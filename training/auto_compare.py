#!/usr/bin/env python3
"""
Auto-run comparison when all models are ready
"""
import os
import time
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")

# Expected model files
MODELS_TO_CHECK = [
    "keras_model.h5",                    # Original
    "keras_model_resnet50.h5",
    "keras_model_efficientnetb0.h5",
    "keras_model_custom_cnn.h5"
]

print("=" * 70)
print("Model Comparison Auto-Runner")
print("=" * 70)
print(f"\nWaiting for all models to be trained...")
print(f"Checking for: {', '.join(MODELS_TO_CHECK)}\n")

# Check every 30 seconds
check_interval = 30
max_wait_time = 8 * 3600  # 8 hours max wait
start_time = time.time()

while True:
    all_ready = True
    for model_file in MODELS_TO_CHECK:
        model_path = os.path.join(MODEL_DIR, model_file)
        exists = os.path.exists(model_path)
        status = "OK" if exists else "MISSING"
        print(f"[{status}] {model_file}")

    # Check if all exist
    all_exist = all(os.path.exists(os.path.join(MODEL_DIR, m)) for m in MODELS_TO_CHECK)

    if all_exist:
        print("\n" + "=" * 70)
        print("All models found! Starting comparison...")
        print("=" * 70 + "\n")

        # Run comparison
        compare_script = os.path.join(SCRIPT_DIR, "compare_models.py")
        subprocess.run([sys.executable, compare_script], cwd=PROJECT_ROOT)
        break

    # Check timeout
    elapsed = time.time() - start_time
    if elapsed > max_wait_time:
        print(f"\nTimeout! Waited more than {max_wait_time/3600:.1f} hours.")
        break

    # Wait and check again
    print(f"\nChecking again in {check_interval} seconds...\n")
    time.sleep(check_interval)

print("\nDone!")
