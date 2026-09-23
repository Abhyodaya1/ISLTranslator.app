"""
Improved Training Script for ISL Hand Sign Recognition
Features:
- MobileNetV2 transfer learning
- Data augmentation for better generalization
- Learning rate scheduling
- Model checkpointing
- Training visualization
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import os
import matplotlib.pyplot as plt

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 30
LEARNING_RATE = 0.0001


def resolve_epochs(default_epochs):
    override = os.getenv("ISL_EPOCHS")
    if override:
        try:
            return max(1, int(override))
        except ValueError:
            print(f"[WARN] Invalid ISL_EPOCHS '{override}', using default {default_epochs}")

    if os.getenv("ISL_FAST_TRAIN") == "1":
        fast_epochs = os.getenv("ISL_FAST_EPOCHS", "6")
        try:
            return max(1, int(fast_epochs))
        except ValueError:
            print(f"[WARN] Invalid ISL_FAST_EPOCHS '{fast_epochs}', using default {default_epochs}")

    return default_epochs


EPOCHS = resolve_epochs(EPOCHS)

os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 70)
print("[TRAINING] ISL Hand Sign Recognition - Training Script")
print("=" * 70)
print(f"[DATA] Data directory: {DATA_DIR}")
print(f"[DATA] Model directory: {MODEL_DIR}")
print(f"[CONFIG] Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"[CONFIG] Batch size: {BATCH_SIZE}")
print(f"[CONFIG] Epochs: {EPOCHS}")
print("=" * 70)

train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=25,
    width_shift_range=0.25,
    height_shift_range=0.25,
    shear_range=0.15,
    zoom_range=0.25,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode='constant',
    cval=255,
    validation_split=0.2,
    channel_shift_range=0.1
)

val_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)

print("\n[DATA] Loading training data...")
train_data = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

print("[DATA] Loading validation data...")
val_data = val_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

num_classes = len(train_data.class_indices)
print(f"\n[OK] Dataset loaded successfully!")
print(f"[INFO] Number of classes: {num_classes}")
print(f"[INFO] Classes: {list(train_data.class_indices.keys())}")
print(f"[INFO] Training samples: {train_data.samples}")
print(f"[INFO] Validation samples: {val_data.samples}")

labels = list(train_data.class_indices.keys())
labels_path = os.path.join(MODEL_DIR, "labels.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(labels):
        f.write(f"{idx} {label}\n")
print(f"[OK] Labels saved to {labels_path}")

print("\n[BUILD] Building model with MobileNetV2...")

base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("[OK] Model built successfully!")
print("\n" + "=" * 70)
print("[TRAINING] Phase 1: Training with Frozen Base")
print("=" * 70)

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
        patience=8,
        restore_best_weights=True,
        verbose=1
    )
]

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

print("\n" + "=" * 70)
print("[TRAINING] Phase 2: Fine-tuning")
print("=" * 70)

base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

print(f"[UNFREEZE] Unfroze last 30 layers of base model for fine-tuning")

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

history.history['accuracy'].extend(history_fine.history['accuracy'])
history.history['val_accuracy'].extend(history_fine.history['val_accuracy'])
history.history['loss'].extend(history_fine.history['loss'])
history.history['val_loss'].extend(history_fine.history['val_loss'])

final_model_path = os.path.join(MODEL_DIR, "keras_model.h5")
model.save(final_model_path)
print(f"\n[OK] Final model saved to {final_model_path}")

print("\n[PLOT] Generating training plots...")

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
print(f"[OK] Training plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, "training_history.png"))
except Exception:
    pass

print("\n" + "=" * 70)
print("[EVALUATION] Final Evaluation on Validation Set")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n[RESULT] Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"[RESULT] Validation Loss: {val_loss:.4f}")

print("\n" + "=" * 70)
print("[DONE] Training Complete!")
print("=" * 70)
print(f"[FILES] Model saved at: {final_model_path}")
print(f"[FILES] Best model saved at: {os.path.join(MODEL_DIR, 'best_model.h5')}")
print(f"[FILES] Labels saved at: {labels_path}")
print(f"[FILES] Training plots saved at: {plot_path}")
print("\n[NEXT] You can now use 'detect_improved.py' to test the model!")
print("=" * 70)
