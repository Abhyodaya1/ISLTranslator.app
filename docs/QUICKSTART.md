# 🚀 Quick Start Guide - ISL Hand Sign Detection

## ⚡ Just Want to Run It?

```powershell
# 1. Verify setup (optional but recommended)
python test_setup.py

# 2. Run the detector!
python detect_improved.py
```

That's it! Show your hand signs and the system will detect them.

---

## 🎮 Controls

### Main Detection App (`detect_improved.py`)
- **'S'** - Toggle statistics view
- **'Q'** - Quit application

### Data Collection (`collect_data_improved.py`)
- **'S' or SPACE** - Save current hand image
- **'Q'** - Quit collection

---

## 📋 Available Signs

The current model recognizes 7 signs:
1. **A** - Alphabet A
2. **B** - Alphabet B
3. **C** - Alphabet C
4. **Help** - Help gesture
5. **Ok** - OK gesture
6. **ThankYou** - Thank you
7. **Yes** - Yes gesture

---

## 🔧 If You Get Errors

### "Model not found"
```powershell
python train_improved.py
```

### "Camera not opening"
- Close other apps using the camera
- Check camera permissions
- Try unplugging and replugging camera

### "Import errors"
```powershell
pip install tensorflow opencv-python mediapipe pyttsx3 matplotlib numpy
```

---

## 📚 Want to Learn More?

- **README_IMPROVED.md** - Full documentation
- **IMPROVEMENTS.md** - What was changed and why
- **test_setup.py** - Verify your system

---

## 🎯 Common Tasks

### Add a New Sign
```powershell
# 1. Collect data
python collect_data_improved.py
# Enter your sign name (e.g., "Hello")
# Press 'S' 200+ times for different angles

# 2. Retrain model
python train_improved.py
# Wait 10-20 minutes

# 3. Test it!
python detect_improved.py
```

### Improve Accuracy
```powershell
# Collect more data (aim for 200-300 images per sign)
python collect_data_improved.py

# Retrain with more data
python train_improved.py
```

---

## 💡 Tips for Best Results

1. **Good Lighting** - Ensure your hand is well-lit
2. **Clear Background** - Avoid cluttered backgrounds
3. **Steady Hand** - Hold gesture for 2-3 seconds
4. **Camera Distance** - Keep hand 30-60cm from camera
5. **Full Visibility** - Ensure entire hand is in frame

---

## 🎉 That's All!

You're ready to use the ISL Hand Sign Detection System!

**Need help?** Check the full documentation in README_IMPROVED.md
