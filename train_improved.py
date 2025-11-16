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
DATA_DIR = "Data"
MODEL_DIR = "Model"
IMG_SIZE = 224
BATCH_SIZE = 16  # Smaller batch for better generalization
EPOCHS = 30  # More epochs
LEARNING_RATE = 0.0001  # Lower learning rate for stability

# Create model directory
os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 70)
print("🚀 ISL Hand Sign Recognition - Training Script")
print("=" * 70)
print(f"📁 Data directory: {DATA_DIR}")
print(f"📁 Model directory: {MODEL_DIR}")
print(f"🖼️  Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"📦 Batch size: {BATCH_SIZE}")
print(f"🔄 Epochs: {EPOCHS}")
print("=" * 70)

# Data augmentation for training - More aggressive
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=25,          # More rotation
    width_shift_range=0.25,     # More shift
    height_shift_range=0.25,    # More shift
    shear_range=0.15,           # Shear transformation
    zoom_range=0.25,            # More zoom variation
    horizontal_flip=True,       # Flip horizontally
    brightness_range=[0.7, 1.3],# More brightness variation
    fill_mode='constant',       # Fill with white
    cval=255,                   # White color value
    validation_split=0.2,
    channel_shift_range=0.1     # Color variation
)

# Validation data (no augmentation, only rescaling)
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

# Print dataset info
num_classes = len(train_data.class_indices)
print(f"\n✅ Dataset loaded successfully!")
print(f"📋 Number of classes: {num_classes}")
print(f"📋 Classes: {list(train_data.class_indices.keys())}")
print(f"🔢 Training samples: {train_data.samples}")
print(f"🔢 Validation samples: {val_data.samples}")

# Save class labels
labels = list(train_data.class_indices.keys())
labels_path = os.path.join(MODEL_DIR, "labels.txt")
with open(labels_path, "w") as f:
    for idx, label in enumerate(labels):
        f.write(f"{idx} {label}\n")
print(f"✅ Labels saved to {labels_path}")

# Build model with MobileNetV2
print("\n🏗️  Building model...")

# Load MobileNetV2 base (pre-trained on ImageNet)
base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze base model initially
base_model.trainable = False

# Build complete model with stronger regularization
model = models.Sequential([
    # Input layer
    layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
    
    # MobileNetV2 base
    base_model,
    
    # Global pooling
    layers.GlobalAveragePooling2D(),
    
    # Stronger dropout
    layers.Dropout(0.5),
    
    # Dense layer with L2 regularization
    layers.Dense(256, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    
    # Additional dense layer
    layers.Dense(128, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    
    # Output layer
    layers.Dense(num_classes, activation="softmax")
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("✅ Model built successfully!")
print("\n📋 Model Summary:")
model.summary()

# Callbacks with better patience
callbacks = [
    # Save best model
    ModelCheckpoint(
        filepath=os.path.join(MODEL_DIR, "best_model.h5"),
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    
    # Reduce learning rate when stuck
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.3,
        patience=5,
        min_lr=1e-8,
        verbose=1
    ),
    
    # Stop early if no improvement - more patience
    EarlyStopping(
        monitor='val_accuracy',
        patience=8,
        restore_best_weights=True,
        verbose=1
    )
]

# Train the model (Phase 1: Frozen base)
print("\n" + "=" * 70)
print("🚀 Starting Training - Phase 1 (Frozen Base)")
print("=" * 70)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS // 2,  # Train for half the epochs
    callbacks=callbacks,
    verbose=1
)

# Fine-tuning (Phase 2: Unfreeze last layers of base)
print("\n" + "=" * 70)
print("🚀 Starting Training - Phase 2 (Fine-tuning)")
print("=" * 70)

# Unfreeze the last 30 layers of the base model
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

print(f"🔓 Unfroze last 30 layers of base model for fine-tuning")

# Recompile with lower learning rate
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Continue training
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

# Save final model
final_model_path = os.path.join(MODEL_DIR, "keras_model.h5")
model.save(final_model_path)
print(f"\n✅ Final model saved to {final_model_path}")

# Plot training history
print("\n📊 Generating training plots...")

plt.figure(figsize=(12, 4))

# Accuracy plot
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.axvline(x=EPOCHS // 2, color='red', linestyle='--', label='Fine-tuning starts')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
plt.legend()
plt.grid(True)

# Loss plot
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
plot_path = os.path.join(MODEL_DIR, "training_history.png")
plt.savefig(plot_path)
print(f"✅ Training plots saved to {plot_path}")

# Evaluate on validation set
print("\n" + "=" * 70)
print("📊 Final Evaluation on Validation Set")
print("=" * 70)

val_loss, val_accuracy = model.evaluate(val_data, verbose=1)
print(f"\n✅ Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"✅ Validation Loss: {val_loss:.4f}")

print("\n" + "=" * 70)
print("🎉 Training Complete!")
print("=" * 70)
print(f"📁 Model saved at: {final_model_path}")
print(f"📁 Best model saved at: {os.path.join(MODEL_DIR, 'best_model.h5')}")
print(f"📁 Labels saved at: {labels_path}")
print(f"📊 Training plots saved at: {plot_path}")
print("\n✨ You can now use 'detect_improved.py' to test the model!")
print("=" * 70)
