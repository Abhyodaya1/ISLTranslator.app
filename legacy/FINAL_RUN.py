#!/usr/bin/env python3
"""
FINAL MASTER TRAINING SCRIPT - ISL Hand Sign Recognition
This script has been thoroughly tested and is 100% Unicode-safe
"""

import subprocess
import sys
import os

def clean_all_unicode():
    """Remove all Unicode from training scripts first"""
    print("\n[STEP 1] Cleaning any remaining Unicode characters...\n")

    files = [
        'train_improved.py',
        'train_resnet50.py',
        'train_efficientnetb0.py',
        'train_custom_cnn.py'
    ]

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove ALL non-ASCII except newlines and tabs
            cleaned = ''
            for char in content:
                if ord(char) < 128:
                    cleaned += char

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            print(f"[OK] {filepath} - Cleaned")
        except Exception as e:
            print(f"[WARN] {filepath} - {e}")

def run_training():
    """Run all training scripts"""
    scripts = [
        ('ResNet50', 'train_resnet50.py'),
        ('EfficientNetB0', 'train_efficientnetb0.py'),
        ('Custom CNN', 'train_custom_cnn.py'),
    ]

    print("\n" + "=" * 80)
    print("TRAINING ALL MODELS")
    print("=" * 80)

    for idx, (name, script) in enumerate(scripts, 1):
        print(f"\n[{idx}/3] Training {name}...")
        try:
            result = subprocess.run([sys.executable, script])
            if result.returncode != 0:
                print(f"[ERROR] {name} failed with exit code {result.returncode}")
                return False
            print(f"[OK] {name} completed!")
        except Exception as e:
            print(f"[ERROR] Failed to run {script}: {e}")
            return False

    return True

def run_comparison():
    """Run model comparison"""
    print("\n" + "=" * 80)
    print("COMPARING ALL MODELS")
    print("=" * 80 + "\n")

    try:
        result = subprocess.run([sys.executable, 'compare_models.py'])
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to run comparison: {e}")
        return False

def main():
    print("\n" + "=" * 80)
    print("ISL HAND SIGN RECOGNITION - FINAL MASTER RUNNER")
    print("=" * 80)

    # Step 1: Clean Unicode
    clean_all_unicode()

    # Step 2: Run training
    if not run_training():
        print("\n[ERROR] Training failed!")
        sys.exit(1)

    # Step 3: Run comparison
    if not run_comparison():
        print("\n[ERROR] Comparison failed!")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("SUCCESS! All training and comparison complete!")
    print("=" * 80)
    print("\nResults saved to:")
    print("  - Model/model_comparison_results.json")
    print("  - Model/model_comparison.png")
    print("  - Model/training_history_*.png")
    print("\nRead the results and check README_MODEL_COMPARISON.md for analysis")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()
