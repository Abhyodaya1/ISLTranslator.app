# Archived / Legacy Code

This folder contains early prototype scripts, tutorial code, and redundant runners that have been deprecated in favor of the modern MediaPipe and Flask/React architecture.

## Files Archived

| File | Original Purpose | Deprecation Reason | Modern Replacement |
|---|---|---|---|
| `test.py` | Early OpenCV skin-color/motion detector | Low accuracy (60-70%), lighting-sensitive | `detect_improved.py` |
| `test1.py` | `cvzone` based sign detector | Dependency issues with `cvzone` / older TF | `detect_improved.py` |
| `test_fixed.py` | Early MediaPipe hand detection test | Experimental script superseded by production detector | `detect_improved.py` |
| `test_simple.py` | Minimal testing script | Replaced by structured test tools | `tools/test_model.py` |
| `dataCollection.py` | Original `cvzone` data capture script | Uses old bounding box cropping | `tools/collect_data_improved.py` |
| `datacollect.py` | Variant of `dataCollection.py` | Duplicate prototype | `tools/collect_data_improved.py` |
| `train.py` | Initial minimal model training script | Lacks transfer learning, evaluation, and callbacks | `training/train_improved.py` |
| `MASTER_TRAIN_AND_COMPARE.py` | Initial multi-model sequential runner | Superseded by feature-rich CLI orchestrator | `training/run_all_training.py` |
| `FINAL_RUN.py` | Windows terminal ASCII cleaning & runner | Consolidated into unified training and tools suite | `training/run_all_training.py` |

> [!NOTE]
> These files are preserved purely for historical and educational reference. To run or train the current application, use the scripts in the root directory and `training/`.

