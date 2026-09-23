# 🚀 ISL Translator - Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## 📊 Running the Model Comparison

### Step 1: Train Alternative Models

Run each training script in sequence (or in parallel if you have multiple GPUs):

```bash
# Model 1: ResNet50 (Highest Accuracy)
# Expected time: 45-55 min (GPU), 4-5 hours (CPU)
python train_resnet50.py

# Model 2: EfficientNetB0 (Best Balanced)
# Expected time: 24-30 min (GPU), 2-3 hours (CPU)
python train_efficientnetb0.py

# Model 3: Custom CNN (Baseline)
# Expected time: 40-50 min (GPU), 3-4 hours (CPU)
python train_custom_cnn.py
```

### Step 2: Compare All 4 Models

Once all models are trained:

```bash
# Compare MobileNetV2 (original) + 3 new models
python compare_models.py
```

This will:
- ✅ Evaluate accuracy of each model
- ✅ Measure model size and parameters
- ✅ Test inference speed
- ✅ Generate comparison visualization
- ✅ Save results to `Model/model_comparison_results.json`

---

## 📈 View Results

### Results Location:
```
Model/
├── model_comparison_results.json  # JSON metrics
└── model_comparison.png            # Visual comparison
```

### Results Include:
- **Accuracy Comparison**: Bar chart of all 4 models
- **Model Size**: Storage requirements comparison
- **Parameters**: Parameter count visualization
- **Inference Speed**: Processing time comparison

---

## 🧪 Test Individual Models

### Original Model (MobileNetV2):
```bash
python detect_improved.py
```

### All Models Use Same Detection Script
The `detect_improved.py` script can be modified to test different models:

```python
# In detect_improved.py, change:
# model_path = "Model/keras_model.h5"  # Original
model_path = "Model/keras_model_resnet50.h5"  # ResNet50
# model_path = "Model/keras_model_efficientnetb0.h5"  # EfficientNetB0
# model_path = "Model/keras_model_custom_cnn.h5"  # Custom CNN
```

---

## 📊 Detailed Results

See **`README_MODEL_COMPARISON.md`** for comprehensive analysis including:

- Model specifications & architecture
- Parameter counts & model sizes
- Accuracy metrics
- Efficiency comparisons
- Open-source model analysis
- Deployment recommendations
- Performance benchmarks

---

## 🎯 Model Selection Guide

| Use Case | Recommended Model |
|----------|------------------|
| **Mobile App** | MobileNetV2 ⭐ |
| **Maximum Accuracy** | ResNet50 ⭐ |
| **Balanced (Best Overall)** | EfficientNetB0 ⭐ |
| **Learning/Research** | Custom CNN |

---

## ⏱️ Timing Estimates

### Training Time (GPU):
- MobileNetV2 (original): 16-20 min
- ResNet50: 45-55 min
- EfficientNetB0: 24-30 min
- Custom CNN: 40-50 min
- **Total**: ~2-3 hours for all models

### Inference Time (per image):
- MobileNetV2: 15-20 ms (≈50 FPS)
- ResNet50: 40-60 ms (≈16-25 FPS)
- EfficientNetB0: 25-35 ms (≈28-40 FPS) ⭐
- Custom CNN: 30-40 ms (≈25-33 FPS)

---

## 🔧 Troubleshooting

### Out of Memory Error:
```bash
# Reduce batch size in training scripts
BATCH_SIZE = 8  # instead of 16
```

### GPU Not Detected:
```bash
# Check TensorFlow GPU setup
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Slow Training:
```bash
# Use GPU (much faster than CPU)
# Install CUDA and cuDNN for GPU acceleration
```

---

## 📚 File Reference

### Training Scripts:
- `train_simple.py` - Original MobileNetV2 training
- `train_resnet50.py` - ResNet50 training (NEW)
- `train_efficientnetb0.py` - EfficientNetB0 training (NEW)
- `train_custom_cnn.py` - Custom CNN training (NEW)

### Comparison & Testing:
- `compare_models.py` - Compare all 4 models (NEW)
- `detect_improved.py` - Inference/detection script
- `api_server.py` - Flask API server
- `start_app.py` - Run full application

### Documentation:
- `README.md` - Main project overview
- `README_MODEL_COMPARISON.md` - This analysis (NEW)
- `MODEL_DOCUMENTATION.md` - Original model details

---

## 🎯 Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Train new models**: Run the 3 new training scripts
3. **Compare results**: Run `python compare_models.py`
4. **Review analysis**: Open `README_MODEL_COMPARISON.md`
5. **Deploy**: Choose best model for your use case

---

**Estimated Total Time**: 2-3 hours (GPU), 10-15 hours (CPU)
**Disk Space Needed**: ~2 GB for models + training artifacts

