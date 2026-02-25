# Synthetic Safety Inspector: YOLOv8 Helmet Detection
An end-to-end computer vision pipeline using Blender-generated synthetic data to train a YOLOv8 model for construction site safety monitoring.

## 🚀 Overview
Real-world safety data is often difficult to collect due to privacy and lighting constraints. 
This project solves that by creating a "Data Factory" in Blender that generates thousands of perfectly labeled images with randomized lighting, camera angles, and occlusions.

## 🛠️ Features
- **Synthetic Data Engine:** Python-driven Blender script using the Nishita Sky model for atmospheric randomization.
- **Automated Labeling:** Direct 3D-to-2D coordinate mapping for pixel-perfect YOLO bounding boxes.
- **Negative Sampling:** Explicitly trained on "unsafe" (no helmet) scenarios to reduce false positives.
- **Domain Randomization:** Variable camera height, radius, and focal targets to ensure geometric generalization.
- **Physics-Based Lighting:** Randomized sun elevation, dust density, and air density to force the model to learn geometry over simple color patterns.

## 📊 Results
- **Training Set:** 1,000 synthetic images.
- **Validation:** 80/20 split with 0.995 mAP50 score and 1.0 Recall on the synthetic validation set, demonstrating severe overfitting to synthetic artifacts when tested against real-world domain shifts. 
- **Challenge:** Identified color bias in initial training (Grey vs. Yellow helmets) and a demographic bias (trained on a single character model), providing a roadmap for future iterations using material randomization.

## 🔮 Future Work
- **Domain Randomization:** Implement material randomization for helmet colors to decouple "shape" from "color".
- **Demographic Expansion:** Integrate a broader range of human 3D models (varying skin tones, builds, and heights) to eliminate algorithmmic bias.
- **Scale Variation:** Randomize worker distance and background complexity to improve performance on frone and CCTV footage. 

## 💻 Tech Stack
Python, Blender Python API (bpy), YOLOv8 (Ultralytics)
