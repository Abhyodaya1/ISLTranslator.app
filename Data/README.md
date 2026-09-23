# ISL Dataset Documentation

This directory contains the dataset used for training and evaluating the Indian Sign Language (ISL) recognition models.

## Dataset Structure

```
Data/
├── 1/                   # Digit 1 (560 images)
├── 2/                   # Digit 2 (528 images)
├── 3/                   # Digit 3 (688 images)
├── 5/                   # Digit 5 (672 images)
├── 6/                   # Digit 6 (656 images)
├── A/                   # Letter A (696 images)
├── B/                   # Letter B (150 images)
├── C/                   # Letter C (1,054 images)
├── D/                   # Letter D (704 images)
├── E/                   # Letter E (672 images)
├── Help/                # Word "Help" (138 images)
├── I/                   # Letter I (736 images)
├── J/                   # Letter J (496 images)
├── O/                   # Letter O (784 images)
├── Ok/                  # Word "Ok" (160 images)
├── ThankYou/            # Word "ThankYou" (167 images)
├── Yes/                 # Word "Yes" (151 images)
└── raw/                 # Raw dataset archive (archive.zip)
```

## Specifications

- **Format**: JPEG (`.jpg`)
- **Resolution**: Scaled to `224x224` RGB during training pipeline
- **Color Space**: RGB
- **Classes**: 17 gesture classes currently active (letters, numbers, common conversational phrases)
- **Total Images**: ~9,000 processed samples

## Data Collection & Augmentation

To collect new samples or add a new sign to the dataset:

```bash
python tools/collect_data_improved.py
```

The script uses Google MediaPipe Hands to automatically detect the hand, extract the region with consistent padding, square-pad the aspect ratio, and store it in `Data/<SignName>/`.

During model training, the following data augmentation operations are applied automatically:
- Rotation: ±15 degrees
- Width & Height Shifts: ±10%
- Shear Range: 0.1
- Zoom Range: 0.1
- Fill Mode: Nearest

