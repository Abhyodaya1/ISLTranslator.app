"""
ResNet50 Transfer Learning Model for ISL Hand Sign Recognition
Features:
- ResNet50 base model (deeper than MobileNetV2)
- 50 layers for better feature extraction
- Optimized for higher accuracy
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU only

import tensorflow as tf

# Prevent GPU memory allocation issues (common cause of exit code 3221225477)
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"[GPU] Found {len(gpus)} GPU(s), memory growth enabled")
    else:
        print("[CPU] No GPU found, using CPU")
except Exception as e:
    print(f"[WARN] GPU config error: {e}")

tf.config.optimizer.set_jit(False)

from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt
import time
import numpy as np

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 8  # Reduced to prevent memory issues
EPOCHS = 25
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
print("[TRAINING] ISL Hand Sign Recognition - ResNet50 Model")
print("=" * 70)
print(f"[DATA] Data directory: {DATA_DIR}")
print(f"[DATA] Model directory: {MODEL_DIR}")
print(f"[CONFIG] Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"[CONFIG] Batch size: {BATCH_SIZE}")
print(f"[CONFIG] Epochs: {EPOCHS}")
print(f"TensorFlow: {tf.__version__}")
print("=" * 70)

# Data augmentation layers (Keras 3.x compatible)
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.2),
])

# Load datasets using new API
print("\n Loading training data...")
train_data = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

print(" Loading validation data...")
val_data = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# Get class names
class_names = train_data.class_names
num_classes = len(class_names)

# Normalize data (0-255 -> 0-1)
normalization_layer = layers.Rescaling(1./255)

# Apply augmentation to training data
train_data = train_data.map(lambda x, y: (data_augmentation(x, training=True), y))
train_data = train_data.map(lambda x, y: (normalization_layer(x), y))

# Only normalize validation data (no augmentation)
val_data = val_data.map(lambda x, y: (normalization_layer(x), y))

# Prefetch for performance
train_data = train_data.prefetch(buffer_size=tf.data.AUTOTUNE)
val_data = val_data.prefetch(buffer_size=tf.data.AUTOTUNE)

print(f"\n[OK] Dataset loaded successfully!")
print(f"[INFO] Number of classes: {num_classes}")
print(f"[INFO] Classes: {class_names}")

# Save labels
labels_path = os.path.join(MODEL_DIR, "labels_resnet50.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(class_names):
        f.write(f"{idx} {label}\n")
print(f"[OK] Labels saved to {labels_path}")

# Build ResNet50 model
print("\n[BUILD] Building ResNet50 model...")

inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

base_model = tf.keras.applications.ResNet50(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights=None  # Train from scratch due to Keras 3.x compatibility issue
)
base_model.trainable = False

x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.4)(x)
x = layers.Dense(256, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.0005))(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.4)(x)
x = layers.Dense(128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.0005))(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=False
)

print("[OK] Model built successfully!")
print(f"[NUM] Total parameters: {model.count_params():,}")
model.summary()

# Callbacks
callbacks = [
    ModelCheckpoint(
        filepath=os.path.join(MODEL_DIR, "best_model_resnet50.h5"),
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

# Training
print("\n" + "=" * 70)
print(" Phase 1: Training ResNet50 with Frozen Base")
print("=" * 70)

start_time = time.time()

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

# Fine-tuning
print("\n" + "=" * 70)
print(" Phase 2: Fine-tuning ResNet50")
print("=" * 70)

base_model.trainable = True
for layer in base_model.layers[:-50]:
    layer.trainable = False

print(f"[UNFREEZE] Unfroze last 50 layers for fine-tuning")

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=False
)

fine_tune_batch = max(1, BATCH_SIZE // 2)
train_data_fine = train_data.unbatch().batch(fine_tune_batch).prefetch(buffer_size=tf.data.AUTOTUNE)
val_data_fine = val_data.unbatch().batch(fine_tune_batch).prefetch(buffer_size=tf.data.AUTOTUNE)
print(f"[TUNE] Fine-tune batch size: {fine_tune_batch}")

history_fine = model.fit(
    train_data_fine,
    validation_data=val_data_fine,
    epochs=EPOCHS // 2,
    callbacks=callbacks,
    verbose=1
)

training_time = time.time() - start_time

# Combine histories
history.history['accuracy'].extend(history_fine.history['accuracy'])
history.history['val_accuracy'].extend(history_fine.history['val_accuracy'])
history.history['loss'].extend(history_fine.history['loss'])
history.history['val_loss'].extend(history_fine.history['val_loss'])

# Save model
model_path = os.path.join(MODEL_DIR, "keras_model_resnet50.h5")
model.save(model_path)
print(f"\n[OK] Final model saved to {model_path}")

# Plot training history
print("\n Generating training plots...")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('ResNet50 - Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('ResNet50 - Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, "training_history_resnet50.png")
plt.savefig(plot_path)
print(f"[OK] Training plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, "training_history_resnet50.png"))
except Exception:
    pass

# Final evaluation
print("\n" + "=" * 70)
print(" Final Evaluation - ResNet50")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n[OK] Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"[OK] Validation Loss: {val_loss:.4f}")
print(f"[TIME] Training Time: {training_time/60:.2f} minutes")

print("\n" + "=" * 70)
print("[SUCCESS] ResNet50 Training Complete!")
print("=" * 70)
