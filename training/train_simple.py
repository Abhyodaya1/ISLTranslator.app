"""
Enhanced Training Script for ISL Hand Sign Recognition
Features:
- MobileNetV2 transfer learning
- Data augmentation for better generalization
- Learning rate scheduling
- Model checkpointing
- Training visualization
- Two-phase training (frozen base + fine-tuning)
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
tf.config.optimizer.set_jit(False)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 16  # Smaller batch for better accuracy with less data
EPOCHS = 25  # More epochs for smaller dataset
LEARNING_RATE = 0.0001

print("=" * 70)
print("🚀 ISL Hand Sign Recognition - Enhanced Training")
print("=" * 70)
print(f"📁 Data directory: {DATA_DIR}")
print(f"📁 Model directory: {MODEL_DIR}")
print(f"🖼️  Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"📦 Batch size: {BATCH_SIZE}")
print(f"🔄 Epochs: {EPOCHS}")
print(f"TensorFlow: {tf.__version__}")
print("=" * 70)

# Data augmentation for training (stronger for smaller dataset)
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=25,
    width_shift_range=0.25,
    height_shift_range=0.25,
    zoom_range=0.25,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='constant',
    cval=255,
    validation_split=0.2
)

# Validation data (no augmentation)
val_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)

# Load training data
print("\n📊 Loading training data...")
train_data = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

# Load validation data
print("📊 Loading validation data...")
val_data = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

num_classes = len(train_data.class_indices)
print(f"\n✅ Dataset loaded successfully!")
print(f"📋 Number of classes: {num_classes}")
print(f"📋 Classes: {list(train_data.class_indices.keys())}")
print(f"🔢 Training samples: {train_data.samples}")
print(f"🔢 Validation samples: {val_data.samples}")

# Save labels
labels = list(train_data.class_indices.keys())
labels_path = os.path.join(MODEL_DIR, "labels.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(labels):
        f.write(f"{idx} {label}\n")
print(f"✅ Labels saved to {labels_path}")

# Build model
print("\n🏗️  Building model...")

# Use functional API
inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False

x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.0005))(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=True
)

print("✅ Model built successfully!")
model.summary()

# Callbacks
callbacks = [
    ModelCheckpoint(
        filepath=os.path.join(MODEL_DIR, "best_model.h5"),
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=4,
        min_lr=1e-7,
        verbose=1
    ),
    EarlyStopping(
        monitor='val_accuracy',
        patience=7,
        restore_best_weights=True,
        verbose=1
    )
]

# Phase 1: Train with frozen base
print("\n" + "=" * 70)
print("🚀 Phase 1: Training with Frozen Base")
print("=" * 70)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

# Phase 2: Fine-tuning
print("\n" + "=" * 70)
print("🚀 Phase 2: Fine-tuning")
print("=" * 70)

base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

print(f"🔓 Unfroze last 30 layers for fine-tuning")

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=True
)

history_fine = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

# Combine histories
history.history['accuracy'].extend(history_fine.history['accuracy'])
history.history['val_accuracy'].extend(history_fine.history['val_accuracy'])
history.history['loss'].extend(history_fine.history['loss'])
history.history['val_loss'].extend(history_fine.history['val_loss'])

# Save model
model_path = os.path.join(MODEL_DIR, "keras_model.h5")
model.save(model_path)
print(f"\n✅ Final model saved to {model_path}")

# Plot training history
print("\n📊 Generating training plots...")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, "training_history.png")
plt.savefig(plot_path)
print(f"✅ Training plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, "training_history.png"))
except Exception:
    pass

# Final evaluation
print("\n" + "=" * 70)
print("📊 Final Evaluation")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n✅ Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"✅ Validation Loss: {val_loss:.4f}")

print("\n" + "=" * 70)
print("🎉 Training Complete!")
print("=" * 70)
print(f"📁 Model: {model_path}")
print(f"📁 Best model: {os.path.join(MODEL_DIR, 'best_model.h5')}")
print(f"📁 Labels: {labels_path}")
print(f"📊 Plots: {plot_path}")
print("\n✨ Test with: python detect_improved.py")
print("=" * 70)
