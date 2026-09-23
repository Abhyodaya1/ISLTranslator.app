# Run Modes for Training and Comparison

This document explains the run modes available in RUN_ALL_MODELS_AND_COMPARE.py and what each mode does.

## Modes

### 1) Fast mode (default)
Command:

python RUN_ALL_MODELS_AND_COMPARE.py

What it does:
- Runs all four trainings with a small number of epochs (default 6).
- Produces results quickly for smoke testing or quick comparisons.
- Still runs the full comparison step and saves JSON + image outputs.

How to change fast epochs:

python RUN_ALL_MODELS_AND_COMPARE.py --fast-epochs 8

### 2) Full mode
Command:

python RUN_ALL_MODELS_AND_COMPARE.py --full

What it does:
- Runs all trainings with the original epoch settings per model.
- Uses the default epochs configured in each training script.
- Best for final results, but takes longer.

### 3) Override epochs (custom mode)
Command:

python RUN_ALL_MODELS_AND_COMPARE.py --epochs 10

What it does:
- Forces the same epoch count for all models.
- Useful for controlled comparisons at a fixed training budget.
- Skips fast mode and full mode defaults.

## Outputs

All modes produce the same output files:
- Model/model_comparison_results.json
- Model/model_comparison.png
- Model/training_history_*.png

The comparison table also includes:
- Epochs used
- Training samples
- Validation samples
- Accuracy, loss, parameters, size, and inference time

## Notes

- If any model script fails, the run stops and the comparison will not execute.
- Dataset counts are collected from the Data folder using the same validation split (0.2).
