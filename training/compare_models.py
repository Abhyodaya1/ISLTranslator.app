"""
Comprehensive Model Comparison Script
Tests all models and generates comparison metrics
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import time
from pathlib import Path
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Configuration
DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 16

# Model paths
MODELS = {
    'MobileNetV2': {
        'path': os.path.join(MODEL_DIR, 'keras_model.h5'),
        'labels': os.path.join(MODEL_DIR, 'labels.txt'),
        'color': '#1f77b4'
    },
    'ResNet50': {
        'path': os.path.join(MODEL_DIR, 'keras_model_resnet50.h5'),
        'labels': os.path.join(MODEL_DIR, 'labels_resnet50.txt'),
        'color': '#ff7f0e'
    },
    'EfficientNetB0': {
        'path': os.path.join(MODEL_DIR, 'keras_model_efficientnetb0.h5'),
        'labels': os.path.join(MODEL_DIR, 'labels_efficientnetb0.txt'),
        'color': '#2ca02c'
    },
    'VGCC': {
        'path': os.path.join(MODEL_DIR, 'keras_model_vgcc.h5'),
        'labels': os.path.join(MODEL_DIR, 'labels_vgcc.txt'),
        'color': '#8c564b'
    },
    'Custom CNN': {
        'path': os.path.join(MODEL_DIR, 'keras_model_custom_cnn.h5'),
        'labels': os.path.join(MODEL_DIR, 'labels_custom_cnn.txt'),
        'color': '#d62728'
    }
}

print("=" * 80)
print("🤖 ISL Hand Sign Recognition - Model Comparison")
print("=" * 80)

# Load test data
print("\n📊 Loading test data...")
val_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)
val_data = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

print(f"✅ Test data loaded: {val_data.samples} samples")

# Results storage
results = {}

# Optional training metadata
metadata = {}
metadata_path = os.path.join(OUTPUT_DIR, 'training_run_metadata.json')
if not os.path.exists(metadata_path):
    metadata_path = os.path.join(MODEL_DIR, 'training_run_metadata.json')
if os.path.exists(metadata_path):
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to read metadata: {e}")

# Test each model
for model_name, model_info in MODELS.items():
    print(f"\n{'=' * 80}")
    print(f"Testing {model_name}")
    print(f"{'=' * 80}")

    # Check if model exists
    if not os.path.exists(model_info['path']):
        print(f"❌ Model not found: {model_info['path']}")
        continue

    try:
        # Load model
        print(f"📁 Loading model from {model_info['path']}...")
        model = tf.keras.models.load_model(model_info['path'])

        # Get model info
        total_params = model.count_params()
        print(f"📊 Total Parameters: {total_params:,}")

        # Calculate model size
        model_size_mb = os.path.getsize(model_info['path']) / (1024 * 1024)
        print(f"💾 Model Size: {model_size_mb:.2f} MB")

        # Evaluate on test data
        print(f"🧪 Evaluating on {val_data.samples} test samples...")

        # Time the evaluation
        start_time = time.time()
        val_loss, val_accuracy = model.evaluate(val_data, verbose=0)
        inference_time = (time.time() - start_time) / val_data.samples * 1000  # ms per sample

        print(f"✅ Validation Accuracy: {val_accuracy * 100:.2f}%")
        print(f"✅ Validation Loss: {val_loss:.4f}")
        print(f"⏱️  Avg Inference Time: {inference_time:.2f} ms/sample")

        # Get per-class accuracy
        print(f"\n📈 Per-class Analysis...")
        val_data.reset()
        predictions = model.predict(val_data, verbose=0)
        true_labels = val_data.classes

        per_class_accuracy = {}
        num_classes = predictions.shape[1]
        for class_idx in range(num_classes):
            class_mask = true_labels == class_idx
            if class_mask.sum() > 0:
                class_preds = np.argmax(predictions[class_mask], axis=1)
                class_acc = np.mean(class_preds == class_idx)
                per_class_accuracy[class_idx] = class_acc

        # Store results
        meta = metadata.get('models', {}).get(model_name, {})
        results[model_name] = {
            'accuracy': val_accuracy,
            'loss': val_loss,
            'parameters': total_params,
            'model_size_mb': model_size_mb,
            'inference_time_ms': inference_time,
            'per_class_accuracy': per_class_accuracy,
            'epochs': meta.get('epochs'),
            'train_samples': meta.get('train_samples'),
            'val_samples': meta.get('val_samples')
        }

        print(f"✅ {model_name} evaluation complete!")

    except Exception as e:
        print(f"❌ Error evaluating {model_name}: {str(e)}")

print(f"\n{'=' * 80}")
print("📊 COMPARISON SUMMARY")
print(f"{'=' * 80}")

# Create comparison table
comparison_data = {
    'Model': [],
    'Epochs': [],
    'Train Samples': [],
    'Val Samples': [],
    'Accuracy (%)': [],
    'Loss': [],
    'Parameters': [],
    'Model Size (MB)': [],
    'Inference Time (ms)': []
}

for model_name, metrics in results.items():
    comparison_data['Model'].append(model_name)
    comparison_data['Epochs'].append(str(metrics.get('epochs', 'N/A')))
    comparison_data['Train Samples'].append(str(metrics.get('train_samples', 'N/A')))
    comparison_data['Val Samples'].append(str(metrics.get('val_samples', 'N/A')))
    comparison_data['Accuracy (%)'].append(f"{metrics['accuracy'] * 100:.2f}")
    comparison_data['Loss'].append(f"{metrics['loss']:.4f}")
    comparison_data['Parameters'].append(f"{metrics['parameters']:,}")
    comparison_data['Model Size (MB)'].append(f"{metrics['model_size_mb']:.2f}")
    comparison_data['Inference Time (ms)'].append(f"{metrics['inference_time_ms']:.2f}")

# Print table
print("\n")
print("Model".ljust(18), "Epochs".ljust(8), "Train".ljust(10), "Val".ljust(10),
    "Accuracy".ljust(12), "Loss".ljust(12), "Parameters".ljust(18),
    "Size (MB)".ljust(12), "Inference (ms)".ljust(15))
print("-" * 100)

best_accuracy = max(results.values(), key=lambda x: x['accuracy'])['accuracy']
best_efficiency = min(results.values(), key=lambda x: x['model_size_mb'])['model_size_mb']

for model_name, metrics in results.items():
    acc_str = f"{metrics['accuracy'] * 100:.2f}%"
    if metrics['accuracy'] == best_accuracy:
        acc_str += " ⭐"

    size_str = f"{metrics['model_size_mb']:.2f}"
    if metrics['model_size_mb'] == best_efficiency:
        size_str += " ⭐"

    print(
        model_name.ljust(18),
        str(metrics.get('epochs', 'N/A')).ljust(8),
        str(metrics.get('train_samples', 'N/A')).ljust(10),
        str(metrics.get('val_samples', 'N/A')).ljust(10),
        acc_str.ljust(12),
        f"{metrics['loss']:.4f}".ljust(12),
        f"{metrics['parameters']:,}".ljust(18),
        size_str.ljust(12),
        f"{metrics['inference_time_ms']:.2f}".ljust(15)
    )

print("-" * 100)
print("⭐ = Best performer in category")

# Save results to JSON
results_path = os.path.join(OUTPUT_DIR, 'model_comparison_results.json')
with open(results_path, 'w') as f:
    json.dump(
        {k: {kk: float(vv) if isinstance(vv, (np.floating, float)) else vv
             for kk, vv in v.items()}
         for k, v in results.items()},
        f,
        indent=2
    )
print(f"\n✅ Results saved to {results_path}")
try:
    with open(os.path.join(MODEL_DIR, 'model_comparison_results.json'), 'w') as f:
        json.dump({k: {kk: float(vv) if isinstance(vv, (np.floating, float)) else vv for kk, vv in v.items()} for k, v in results.items()}, f, indent=2)
except Exception:
    pass

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Accuracy comparison
ax = axes[0, 0]
models_list = list(results.keys())
accuracies = [results[m]['accuracy'] * 100 for m in models_list]
colors = [MODELS[m]['color'] for m in models_list]
ax.bar(models_list, accuracies, color=colors, alpha=0.7)
ax.set_ylabel('Accuracy (%)')
ax.set_title('Model Accuracy Comparison')
ax.set_ylim([0, 100])
for i, v in enumerate(accuracies):
    ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom')
ax.grid(axis='y', alpha=0.3)

# Model size comparison
ax = axes[0, 1]
sizes = [results[m]['model_size_mb'] for m in models_list]
ax.bar(models_list, sizes, color=colors, alpha=0.7)
ax.set_ylabel('Size (MB)')
ax.set_title('Model Size Comparison')
for i, v in enumerate(sizes):
    ax.text(i, v + 0.3, f'{v:.1f}MB', ha='center', va='bottom')
ax.grid(axis='y', alpha=0.3)

# Parameters comparison
ax = axes[1, 0]
params = [results[m]['parameters'] / 1e6 for m in models_list]
ax.bar(models_list, params, color=colors, alpha=0.7)
ax.set_ylabel('Parameters (Millions)')
ax.set_title('Model Parameters Comparison')
for i, v in enumerate(params):
    ax.text(i, v + 0.1, f'{v:.1f}M', ha='center', va='bottom')
ax.grid(axis='y', alpha=0.3)

# Inference time comparison
ax = axes[1, 1]
times = [results[m]['inference_time_ms'] for m in models_list]
ax.bar(models_list, times, color=colors, alpha=0.7)
ax.set_ylabel('Time (ms)')
ax.set_title('Inference Time Comparison')
for i, v in enumerate(times):
    ax.text(i, v + 0.5, f'{v:.2f}ms', ha='center', va='bottom')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, 'model_comparison.png')
plt.savefig(plot_path, dpi=150)
print(f"✅ Comparison plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, 'model_comparison.png'), dpi=150)
except Exception:
    pass

print(f"\n{'=' * 80}")
print("🎉 Model Comparison Complete!")
print(f"{'=' * 80}")
