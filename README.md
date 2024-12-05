# OCR for Everytime Dataset: Project Overview

## Project Description

This study focuses on developing a cutting-edge **Optical Character Recognition (OCR)** technology optimized for the **Everytime dataset**, employing a novel deep learning-based hybrid architecture. Key components of the model include:

- **CTPN (Connectionist Text Proposal Network):** Efficient text detection in images.
- **TPS-ResNet-BiLSTM-Attn (Thin-Plate Spline Spatial Transformer Network, Residual Network, Bidirectional Long Short-Term Memory, Attention):** Accurate recognition of detected text.
- **HangulNet Module:** Specialized for Korean text, decomposing Hangul characters into consonants and vowels for enhanced recognition accuracy.

### Challenges Addressed:
- Complex structure of Korean characters.
- Improved OCR performance specific to the Everytime dataset.

---

## Repository Structure

```plaintext
├── dataset.py           # Custom dataset class for Everytime OCR dataset
├── model.py             # CRNN-based OCR model implementation
├── train.py             # Training script for OCR model
├── make_dataset.py      # Script to generate synthetic timetable datasets
├── README.md            # Project documentation
└── test_datasets/       # Folder containing generated synthetic datasets
