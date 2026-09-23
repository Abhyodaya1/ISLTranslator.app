#!/usr/bin/env python3
"""
Run all model trainings (MobileNetV2, ResNet50, EfficientNetB0, Custom CNN)
then compare all models to produce table output, JSON, and image results.
"""

import argparse
import os
import sys
import subprocess
import time

from tensorflow.keras.preprocessing.image import ImageDataGenerator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
IMG_SIZE = 224
VALIDATION_SPLIT = 0.2

TRAINING_SCRIPTS = [
    ("MobileNetV2", "train_improved.py"),
    ("ResNet50", "train_resnet50.py"),
    ("EfficientNetB0", "train_efficientnetb0.py"),
    ("VGCC", "train_vgcc.py"),
    ("Custom CNN", "train_custom_cnn.py"),
]

COMPARE_SCRIPT = "compare_models.py"

DEFAULT_EPOCHS = {
    "MobileNetV2": 30,
    "ResNet50": 25,
    "EfficientNetB0": 25,
    "VGCC": 25,
    "Custom CNN": 25,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run all model trainings and compare results.")
    parser.add_argument("--full", action="store_true", help="Run full training (no fast mode).")
    parser.add_argument("--epochs", type=int, help="Override epochs for all models.")
    parser.add_argument("--fast-epochs", type=int, default=6, help="Epochs to use in fast mode.")
    return parser.parse_args()


def verify_scripts():
    missing = []
    for _, script in TRAINING_SCRIPTS:
        if not os.path.exists(script):
            missing.append(script)
    if not os.path.exists(COMPARE_SCRIPT):
        missing.append(COMPARE_SCRIPT)

    if missing:
        print("[ERROR] Missing required script(s):")
        for script in missing:
            print(f"  - {script}")
        return False
    return True


def collect_dataset_counts():
    datagen = ImageDataGenerator(rescale=1.0 / 255, validation_split=VALIDATION_SPLIT)
    train_data = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=16,
        class_mode="categorical",
        subset="training",
        shuffle=False
    )
    val_data = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=16,
        class_mode="categorical",
        subset="validation",
        shuffle=False
    )
    return train_data.samples, val_data.samples


def write_training_metadata(epochs_by_model, train_samples, val_samples):
    os.makedirs(MODEL_DIR, exist_ok=True)
    metadata = {
        "data_dir": DATA_DIR,
        "image_size": IMG_SIZE,
        "validation_split": VALIDATION_SPLIT,
        "models": {}
    }

    for model_name, epochs in epochs_by_model.items():
        metadata["models"][model_name] = {
            "epochs": epochs,
            "train_samples": train_samples,
            "val_samples": val_samples
        }

    metadata_path = os.path.join(MODEL_DIR, "training_run_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        import json
        json.dump(metadata, f, indent=2)

    print(f"[OK] Training metadata saved to {metadata_path}")


def run_training(env):
    print("=" * 80)
    print("TRAINING ALL MODELS")
    print("=" * 80)

    for idx, (name, script) in enumerate(TRAINING_SCRIPTS, 1):
        print(f"\n[{idx}/{len(TRAINING_SCRIPTS)}] Training {name}...")
        start = time.time()
        script_path = os.path.join(SCRIPT_DIR, script)
        result = subprocess.run([sys.executable, script_path], env=env, cwd=PROJECT_ROOT)
        elapsed = (time.time() - start) / 60
        if result.returncode != 0:
            print(f"[ERROR] {name} failed with exit code {result.returncode}")
            return False
        print(f"[OK] {name} completed in {elapsed:.1f} minutes")

    return True


def run_comparison():
    print("\n" + "=" * 80)
    print("COMPARING ALL MODELS")
    print("=" * 80 + "\n")

    compare_path = os.path.join(SCRIPT_DIR, COMPARE_SCRIPT)
    result = subprocess.run([sys.executable, compare_path], cwd=PROJECT_ROOT)
    return result.returncode == 0


def main():
    print("=" * 80)
    print("ISL HAND SIGN RECOGNITION - RUN ALL MODELS AND COMPARE")
    print("=" * 80)

    args = parse_args()
    fast_mode = not args.full and args.epochs is None
    epochs_override = args.epochs
    fast_epochs = max(1, args.fast_epochs)

    env = os.environ.copy()
    if fast_mode:
        env["ISL_FAST_TRAIN"] = "1"
        env["ISL_FAST_EPOCHS"] = str(fast_epochs)
        print(f"[FAST] Fast training enabled: {fast_epochs} epochs")
    elif epochs_override is not None:
        env["ISL_EPOCHS"] = str(max(1, epochs_override))
        print(f"[OVERRIDE] Epochs set to {epochs_override} for all models")
    else:
        print("[FULL] Full training enabled")

    if not verify_scripts():
        sys.exit(1)

    train_samples, val_samples = collect_dataset_counts()
    if epochs_override is not None:
        epochs_by_model = {name: max(1, epochs_override) for name, _ in TRAINING_SCRIPTS}
    elif fast_mode:
        epochs_by_model = {name: fast_epochs for name, _ in TRAINING_SCRIPTS}
    else:
        epochs_by_model = DEFAULT_EPOCHS.copy()

    write_training_metadata(epochs_by_model, train_samples, val_samples)

    if not run_training(env):
        print("\n[ERROR] Training failed.")
        sys.exit(1)

    if not run_comparison():
        print("\n[ERROR] Comparison failed.")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("SUCCESS! All training and comparison complete!")
    print("=" * 80)
    print("\nResults saved to:")
    print("  - Model/model_comparison_results.json")
    print("  - Model/model_comparison.png")
    print("  - Model/training_history_*.png")
    print("\nRead README_MODEL_COMPARISON.md for analysis.")


if __name__ == "__main__":
    main()
