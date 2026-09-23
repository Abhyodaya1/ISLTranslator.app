"""
Custom CNN Model from Scratch for ISL Hand Sign Recognition
Features:
- Built from scratch (no transfer learning)
- Custom architecture optimized for hand signs
- Good baseline for comparison
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
LEARNING_RATE = 0.001


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
print("[TRAINING] ISL Hand Sign Recognition - Custom CNN Model")
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
labels_path = os.path.join(MODEL_DIR, "labels_custom_cnn.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(labels):
        f.write(f"{idx} {label}\n")
print(f"[OK] Labels saved to {labels_path}")

# Build Custom CNN model
print("\n[BUILD] Building Custom CNN model...")

model = models.Sequential([
    # Input layer
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),

    # Block 1
    layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Block 2
    layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Block 3
    layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Block 4
    layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),

    # Block 5
    layers.Conv2D(512, (3, 3), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.GlobalAveragePooling2D(),

    # Dense layers
    layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.0005)),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.0005)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

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
        filepath=os.path.join(MODEL_DIR, "best_model_custom_cnn.h5"),
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
print(" Training Custom CNN")
print("=" * 70)

start_time = time.time()

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

training_time = time.time() - start_time

# Save model
model_path = os.path.join(MODEL_DIR, "keras_model_custom_cnn.h5")
model.save(model_path)
print(f"\n[OK] Final model saved to {model_path}")

# Plot training history
print("\n Generating training plots...")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Custom CNN - Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Custom CNN - Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, "training_history_custom_cnn.png")
plt.savefig(plot_path)
print(f"[OK] Training plots saved to {plot_path}")
try:
    plt.savefig(os.path.join(MODEL_DIR, "training_history_custom_cnn.png"))
except Exception:
    pass

# Final evaluation
print("\n" + "=" * 70)
print("[EVAL] Final Evaluation - Custom CNN")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n[OK] Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"[OK] Validation Loss: {val_loss:.4f}")
print(f"[TIME] Training Time: {training_time/60:.2f} minutes")

print("\n" + "=" * 70)
print("[SUCCESS] Custom CNN Training Complete!")
print("=" * 70)
