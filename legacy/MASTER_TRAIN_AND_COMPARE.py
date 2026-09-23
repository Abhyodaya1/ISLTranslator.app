#!/usr/bin/env python3
"""
MASTER TRAINING RUNNER
Trains all 4 models sequentially and runs comparison
"""

import subprocess
import sys
import os
import time

print("=" * 80)
print("[START] ISL Translator - Master Training Runner")
print("=" * 80)

# Check if all input files exist
print("\n[CHECK] Verifying training scripts...")
scripts_to_run = [
    ('ResNet50', 'train_resnet50.py'),
    ('EfficientNetB0', 'train_efficientnetb0.py'),
    ('Custom CNN', 'train_custom_cnn.py'),
]

for name, script in scripts_to_run:
    if os.path.exists(script):
        print(f"[OK] {script} - Ready")
    else:
        print(f"[ERROR] {script} - NOT FOUND")
        sys.exit(1)

print(f"\n[INFO] Will train {len(scripts_to_run)} models")
print("[INFO] Total estimated time: 2-3 hours (GPU), 10-15 hours (CPU)\n")

# Run training scripts
total_start = time.time()

for idx, (model_name, script_name) in enumerate(scripts_to_run, 1):
    print("\n" + "=" * 80)
    print(f"[{idx}/{len(scripts_to_run)}] TRAINING: {model_name}")
    print("=" * 80)

    start_time = time.time()

    try:
        print(f"[RUN] python {script_name}\n")
        result = subprocess.run([sys.executable, script_name])

        elapsed = (time.time() - start_time) / 60

        if result.returncode == 0:
            print(f"\n[SUCCESS] {model_name} training completed in {elapsed:.1f} minutes")
        else:
            print(f"\n[FAILURE] {model_name} training failed with exit code {result.returncode}")
            sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Exception running {script_name}: {e}")
        sys.exit(1)

# Run model comparison
print("\n" + "=" * 80)
print("[FINAL] RUNNING MODEL COMPARISON")
print("=" * 80)

try:
    print("[RUN] python compare_models.py\n")
    result = subprocess.run([sys.executable, 'compare_models.py'])

    if result.returncode == 0:
        print("\n[SUCCESS] Model comparison completed!")
        print("\n[SAVED] Results:")
        print("  - Model/model_comparison_results.json")
        print("  - Model/model_comparison.png")
    else:
        print(f"\n[FAILURE] Comparison failed with exit code {result.returncode}")
        sys.exit(1)

except Exception as e:
    print(f"\n[ERROR] Exception running comparison: {e}")
    sys.exit(1)

total_elapsed = (time.time() - total_start) / 60
print("\n" + "=" * 80)
print("[DONE] All training and comparison complete!")
print(f"[TIME] Total time: {total_elapsed:.1f} minutes ({total_elapsed/60:.1f} hours)")
print("=" * 80)
print("\nNext steps:")
print("1. Review Model/model_comparison.png for visual comparison")
print("2. Check Model/model_comparison_results.json for detailed metrics")
print("3. Read README_MODEL_COMPARISON.md for analysis")
print("\n[END]")
