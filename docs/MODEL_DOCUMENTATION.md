# ISL Hand Sign Recognition Model - Technical Documentation

## Overview

This project uses a **MobileNetV2-based transfer learning model** to recognize Indian Sign Language (ISL) hand signs in real-time. The model is trained using TensorFlow/Keras and can classify 17 different hand signs with high accuracy.

---

## Model Architecture

### Base Model: MobileNetV2

**MobileNetV2** is a lightweight convolutional neural network designed for mobile and embedded vision applications.

**Why MobileNetV2?**
- **Efficient**: Only 2.26M parameters (frozen), making it fast for real-time inference
- **Pre-trained**: Uses ImageNet weights, providing robust feature extraction
- **Accurate**: Inverted residual structure with linear bottlenecks for better feature representation
- **Fast**: Optimized for speed without sacrificing accuracy

**Input Shape**: `224x224x3` (RGB images)
**Output**: `7x7x1280` feature maps

### Custom Classification Head

Built on top of MobileNetV2:

```
Input (224x224x3)
    ↓
MobileNetV2 Base (frozen)
    ↓
GlobalAveragePooling2D → Converts 7x7x1280 to 1280 features
    ↓
Dropout (0.3) → Prevents overfitting
    ↓
Dense (128 units, ReLU, L2=0.0005) → Feature compression with regularization
    ↓
BatchNormalization → Stabilizes training
    ↓
Dropout (0.3) → Additional regularization
    ↓
Dense (17 units, Softmax) → Final classification layer
```

**Total Parameters**: 2,424,657
- **Trainable**: 166,417 (6.9%)
- **Frozen**: 2,258,240 (93.1%)

---

## Training Process

### Two-Phase Training Strategy

#### **Phase 1: Frozen Base Training (12 epochs)**

**Purpose**: Train only the custom classification head while keeping MobileNetV2 weights frozen.

**Configuration**:
- Learning Rate: `0.0001`
- Optimizer: Adam
- Frozen Layers: All MobileNetV2 layers
- Trainable: Only custom head (166K params)

**Why?**
- Prevents corrupting pre-trained ImageNet features
- Allows custom head to learn ISL-specific patterns
- Faster convergence

#### **Phase 2: Fine-tuning (13 epochs)**

**Purpose**: Unfreeze last 30 layers of MobileNetV2 and fine-tune for ISL specifics.

**Configuration**:
- Learning Rate: `0.00001` (10x lower)
- Unfrozen Layers: Last 30 layers of MobileNetV2
- Total Trainable Params: Higher

**Why?**
- Adapts high-level features to ISL hand shapes
- Lower learning rate prevents catastrophic forgetting
- Improves accuracy by 2-5%

---

## Data Processing Pipeline

### 1. Data Organization

```
Data/
├── 1/          # 560 images
├── 2/          # 528 images
├── 3/          # 688 images
├── 5/          # 672 images
├── 6/          # 656 images
├── A/          # 696 images
├── B/          # 150 images
├── C/          # 1054 images
├── D/          # 704 images
├── E/          # 672 images
├── Help/       # 138 images
├── I/          # 736 images
├── J/          # 496 images
├── O/          # 784 images
├── Ok/         # 160 images
├── ThankYou/   # 167 images
└── Yes/        # 151 images
```

**Total**: ~9,000 images across 17 classes

### 2. Data Augmentation

**Training Data Augmentation** (applied in real-time during training):

```python
ImageDataGenerator(
    rescale=1.0/255,              # Normalize pixel values to [0,1]
    rotation_range=25,            # Random rotation ±25°
    width_shift_range=0.25,       # Horizontal shift ±25%
    height_shift_range=0.25,      # Vertical shift ±25%
    zoom_range=0.25,              # Random zoom 75%-125%
    horizontal_flip=True,         # Mirror flip (50% chance)
    brightness_range=[0.8, 1.2],  # Brightness variation ±20%
    fill_mode='constant',         # Fill empty pixels with white
    cval=255,                     # White color (255)
    validation_split=0.2          # 80% train, 20% validation
)
```

**Why Augmentation?**
- **Increases dataset diversity**: 9K images → effectively millions of variations
- **Prevents overfitting**: Model learns to recognize signs from different angles, lighting, positions
- **Improves generalization**: Works better with new, unseen hand positions
- **Handles real-world conditions**: Different lighting, camera angles, hand positions

**Validation Data** (no augmentation):
```python
ImageDataGenerator(
    rescale=1.0/255,        # Only normalization
    validation_split=0.2
)
```

### 3. Data Split

- **Training Set**: 7,216 images (80%)
- **Validation Set**: 1,796 images (20%)
- **Batch Size**: 16 images per batch

**Why this split?**
- 80/20 is standard for small datasets
- Ensures enough data for both training and validation
- Prevents overfitting by testing on unseen data

---

## Image Processing Flow

### Training Time

```
1. Load image from disk (original size)
        ↓
2. Resize to 224x224 pixels
        ↓
3. Apply random augmentation (rotation, shift, zoom, brightness)
        ↓
4. Normalize pixels (0-255 → 0.0-1.0)
        ↓
5. Batch 16 images together
        ↓
6. Feed to model
```

### Inference Time (Prediction)

```
1. Capture frame from camera/upload
        ↓
2. Detect hand region using MediaPipe (optional)
        ↓
3. Resize to 224x224 pixels
        ↓
4. Normalize pixels (0-255 → 0.0-1.0)
        ↓
5. Add batch dimension (224,224,3) → (1,224,224,3)
        ↓
6. Pass through model
        ↓
7. Get probability distribution (17 values, sum=1.0)
        ↓
8. Return class with highest probability + confidence score
```

---

## Training Configuration

### Loss Function

**Categorical Crossentropy**
- Measures difference between predicted probabilities and true labels
- Formula: `-Σ(y_true * log(y_pred))`
- Lower loss = better predictions

### Optimizer

**Adam (Adaptive Moment Estimation)**
- Learning Rate Phase 1: `0.0001`
- Learning Rate Phase 2: `0.00001`
- Adaptive learning rates for each parameter
- Momentum-based optimization

### Regularization Techniques

1. **L2 Regularization** (`0.0005`)
   - Prevents weights from becoming too large
   - Reduces overfitting

2. **Dropout** (`0.3`)
   - Randomly deactivates 30% of neurons during training
   - Prevents co-adaptation of features
   - Forces network to learn robust features

3. **Batch Normalization**
   - Normalizes activations between layers
   - Stabilizes training
   - Allows higher learning rates

4. **Data Augmentation**
   - Acts as regularization by creating variations
   - Most effective regularization for image data

### Callbacks

#### 1. **ModelCheckpoint**
```python
monitor='val_accuracy'
save_best_only=True
```
- Saves model only when validation accuracy improves
- Keeps best model even if later epochs overfit

#### 2. **ReduceLROnPlateau**
```python
monitor='val_loss'
factor=0.5
patience=4
```
- Reduces learning rate by 50% if validation loss plateaus for 4 epochs
- Helps escape local minima
- Enables finer-tuned optimization

#### 3. **EarlyStopping**
```python
monitor='val_accuracy'
patience=7
restore_best_weights=True
```
- Stops training if no improvement for 7 epochs
- Prevents wasting time and overfitting
- Restores weights from best epoch

---

## Model Outputs

### Prediction Format

```python
# Example prediction
prediction = model.predict(image)
# Output: [[0.02, 0.01, 0.89, 0.03, 0.01, 0.01, 0.01, 0.01, 0.005, ...]]
#         Class 0  1     2     3     4     5     6     7     8
```

**Shape**: `(1, 17)` - Probabilities for each of 17 classes

**Processing**:
```python
class_index = np.argmax(prediction)  # Index of highest probability
confidence = prediction[0][class_index]  # Confidence score (0-1)
label = labels[class_index]  # Class name (e.g., "A", "Help")
```

### Label Mapping

Labels are stored in `Model/labels.txt`:
```
0 1
1 2
2 3
3 5
4 6
5 A
6 B
7 C
8 D
9 E
10 Help
11 I
12 J
13 O
14 Ok
15 ThankYou
16 Yes
```

---

## Model Performance Metrics

### Accuracy
- **Training Accuracy**: How well model predicts on training data
- **Validation Accuracy**: How well model predicts on unseen validation data
- **Target**: >90% validation accuracy

### Loss
- **Training Loss**: Error on training data
- **Validation Loss**: Error on validation data
- **Ideal**: Both losses should decrease and converge

### Overfitting Detection
- **Training Acc >> Validation Acc**: Model memorizing, not learning
- **Solution**: More augmentation, higher dropout, L2 regularization

---

## Model Files

### Output Files

1. **`Model/keras_model.h5`** (9.25 MB)
   - Final trained model
   - Used for inference/predictions
   - Contains architecture + weights

2. **`Model/best_model.h5`** (9.25 MB)
   - Best performing model during training
   - Has highest validation accuracy
   - Backup if final model overfits

3. **`Model/labels.txt`**
   - Class index to label mapping
   - Required for converting predictions to readable text

4. **`Model/training_history.png`**
   - Graphs showing accuracy and loss curves
   - Visual validation of training quality

---

## Inference Speed

**On CPU**: ~50-100ms per prediction
**On GPU**: ~10-20ms per prediction

**Real-time capable**: Yes (>10 FPS)

---

## Model Limitations

1. **Hand Detection**: Model assumes hand is centered in frame (solved by MediaPipe preprocessing)
2. **Lighting**: Very dark/bright conditions may reduce accuracy
3. **Hand Size**: Works best when hand fills ~60-80% of frame
4. **Background**: Complex backgrounds may confuse model (MediaPipe helps)
5. **Static Signs Only**: Cannot recognize dynamic/motion-based signs

---

## Future Improvements

1. **Increase dataset size**: More images per class (target: 1000+ each)
2. **Add more classes**: Expand to full ISL alphabet and numbers
3. **Sequence modeling**: LSTM/Transformer for motion-based signs
4. **Model quantization**: Reduce size for mobile deployment
5. **TensorFlow Lite**: Convert for mobile/edge devices
6. **Multi-hand support**: Recognize two-handed signs

---

## Technical Stack

- **Framework**: TensorFlow 2.20.0 + Keras 3.11.3
- **Python**: 3.12
- **Base Model**: MobileNetV2 (ImageNet pre-trained)
- **Training Mode**: Eager Execution (for Keras 3 compatibility)
- **Hardware**: CPU/GPU compatible
- **Preprocessing**: MediaPipe Hand Detection
- **Deployment**: Flask API + React Frontend

---

## Training Script

**Primary Script**: `train_simple.py`

**Run Training**:
```bash
python train_simple.py
```

**Expected Duration**: 15-20 minutes (CPU), 5-10 minutes (GPU)

**Outputs**:
- Trained model: `Model/keras_model.h5`
- Best model: `Model/best_model.h5`
- Labels: `Model/labels.txt`
- Training plots: `Model/training_history.png`

---

## Model Testing

**Webcam Test**:
```bash
python detect_improved.py
```

**API Server**:
```bash
python api_server.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

---

## References

- **MobileNetV2 Paper**: https://arxiv.org/abs/1801.04381
- **Transfer Learning**: https://cs231n.github.io/transfer-learning/
- **Data Augmentation**: https://www.tensorflow.org/tutorials/images/data_augmentation
- **Keras Documentation**: https://keras.io/

---

*Last Updated: November 17, 2025*
