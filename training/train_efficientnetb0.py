"""
EfficientNetB0 Transfer Learning Model for ISL Hand Sign Recognition
Features:
- EfficientNetB0 base model (excellent parameter efficiency)
- Compound scaling for optimal accuracy/efficiency trade-off
- Lightweight alternative to ResNet50
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf

# Prevent GPU memory allocation issues
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

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt
import time

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
print("[TRAINING] ISL Hand Sign Recognition - EfficientNetB0 Model")
print("=" * 70)
print(f"[DATA] Data directory: {DATA_DIR}")
print(f"[DATA] Model directory: {MODEL_DIR}")
print(f"[CONFIG] Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"[CONFIG] Batch size: {BATCH_SIZE}")
print(f"[CONFIG] Epochs: {EPOCHS}")
print(f"TensorFlow: {tf.__version__}")
print("=" * 70)

# Data augmentation for training
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
print("\n Loading training data...")
train_data = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

# Load validation data
print(" Loading validation data...")
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
print(f"[NUM] Training samples: {train_data.samples}")
print(f"[NUM] Validation samples: {val_data.samples}")

# Save labels
labels = list(train_data.class_indices.keys())
labels_path = os.path.join(MODEL_DIR, "labels_efficientnetb0.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(labels):
        f.write(f"{idx} {label}\n")
print(f"[OK] Labels saved to {labels_path}")

# Build EfficientNetB0 model
print("\n[BUILD] Building EfficientNetB0 model...")

inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

base_model = tf.keras.applications.EfficientNetB0(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights=None  # Train from scratch due to Keras 3.x compatibility issue
)
base_model.trainable = False

x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.35)(x)
x = layers.Dense(256, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.0005))(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.35)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=True
)

print("[OK] Model built successfully!")
print(f"[NUM] Total parameters: {model.count_params():,}")
model.summary()

# Callbacks
callbacks = [
    ModelCheckpoint(
        filepath=os.path.join(MODEL_DIR, "best_model_efficientnetb0.h5"),
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
print(" Phase 1: Training EfficientNetB0 with Frozen Base")
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
print(" Phase 2: Fine-tuning EfficientNetB0")
print("=" * 70)

base_model.trainable = True
for layer in base_model.layers[:-40]:
    layer.trainable = False

print(f"[UNFREEZE] Unfroze last 40 layers for fine-tuning")

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

training_time = time.time() - start_time

# Combine histories
history.history['accuracy'].extend(history_fine.history['accuracy'])
history.history['val_accuracy'].extend(history_fine.history['val_accuracy'])
history.history['loss'].extend(history_fine.history['loss'])
history.history['val_loss'].extend(history_fine.history['val_loss'])

# Save model
model_path = os.path.join(MODEL_DIR, "keras_model_efficientnetb0.h5")
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
plt.title('EfficientNetB0 - Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('EfficientNetB0 - Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, "training_history_efficientnetb0.png")
plt.savefig(plot_path)
print(f"[OK] Training plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, "training_history_efficientnetb0.png"))
except Exception:
    pass

# Final evaluation
print("\n" + "=" * 70)
print("[EVAL] Final Evaluation - EfficientNetB0")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n[OK] Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"[OK] Validation Loss: {val_loss:.4f}")
print(f"[TIME] Training Time: {training_time/60:.2f} minutes")

print("\n" + "=" * 70)
print("[SUCCESS] EfficientNetB0 Training Complete!")
print("=" * 70)
