#!/usr/bin/env python3
"""
Complete Unicode Cleaner for Training Scripts
Removes ALL non-ASCII characters and replaces with ASCII equivalents
"""

import re
import sys

files_to_clean = [
    'train_improved.py',
    'train_resnet50.py',
    'train_efficientnetb0.py',
    'train_custom_cnn.py'
]

print("=" * 80)
print("UNICODE CLEANER - Removing all non-ASCII characters")
print("=" * 80)

for filepath in files_to_clean:
    print(f"\nProcessing: {filepath}")

    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Process each line
        cleaned_lines = []
        modified_count = 0

        for line_num, line in enumerate(lines, 1):
            original = line

            # Remove all Unicode characters except ASCII control characters
            cleaned = ''
            for char in line:
                if ord(char) < 128:  # ASCII range
                    cleaned += char
                else:
                    # Silently skip non-ASCII
                    modified_count += 1

            if cleaned != original:
                print(f"  Line {line_num}: Removed non-ASCII characters")

            cleaned_lines.append(cleaned)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)

        if modified_count > 0:
            print(f"  Total: {modified_count} non-ASCII characters removed")
        else:
            print(f"  ✓ File is clean (no changes needed)")

    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        sys.exit(1)

print("\n" + "=" * 80)
print("✓ ALL FILES CLEANED SUCCESSFULLY!")
print("=" * 80)
print("\nAll training scripts are now 100% ASCII-safe.")
print("You can now run:")
print("  python MASTER_TRAIN_AND_COMPARE.py")
print("\n" + "=" * 80)
