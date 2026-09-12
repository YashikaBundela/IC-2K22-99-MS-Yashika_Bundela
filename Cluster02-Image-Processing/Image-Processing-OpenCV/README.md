# Cluster 02: Image Processing

## Problem Statement
To implement basic image processing operations using Python and OpenCV and
analyze how different transformations affect a digital image.

## Objectives
- Understand basic digital image processing.
- Convert images into grayscale.
- Resize images.
- Apply binary thresholding.
- Reduce image noise using Gaussian blur.
- Detect edges using the Canny algorithm.
- Perform image rotation.
- Store processed images as output files.

## Technologies Used
- Python 3
- OpenCV
- VS Code

## Input
Supported image formats:
- JPG
- JPEG
- PNG
- BMP
- WEBP
- TIFF

Sample input:
```
input/sample.jpg
```

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python image_processing.py input/sample.jpg
```

## Output
Processed images are written to `output/`:

| File              | Operation                          |
|-------------------|-------------------------------------|
| `grayscale.jpg`   | Grayscale conversion                |
| `resized.jpg`     | Resized to 50% of original dimensions |
| `threshold.jpg`   | Binary thresholding (threshold = 127) |
| `blurred.jpg`     | Gaussian blur (5x5 kernel)          |
| `edges.jpg`       | Canny edge detection (100, 200)     |
| `rotated.jpg`     | Rotated 90° clockwise               |

## Project Structure
```
Image-Processing-OpenCV/
├── image_processing.py
├── requirements.txt
├── input/
│   └── sample.jpg
└── output/
    ├── grayscale.jpg
    ├── resized.jpg
    ├── threshold.jpg
    ├── blurred.jpg
    ├── edges.jpg
    └── rotated.jpg
```
