"""
image_enhancement.py
--------------------
Lab 04: Image Enhancement

This program improves an image using different image enhancement
techniques such as:
1. Contrast enhancement
2. Brightness correction
3. Noise reduction
4. Sharpening
5. Image upscaling
6. Combined enhancement

Supported formats:
JPG, JPEG, PNG, BMP, WEBP, TIFF

Usage:
    python image_enhancement.py <path-to-image>
"""

import os
import sys

import cv2
import numpy as np


SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png",
    ".bmp", ".webp",
    ".tif", ".tiff"
}


def load_image(input_path):
    """Load an image using OpenCV."""
    image = cv2.imread(input_path)

    if image is None:
        raise ValueError(
            "Unable to load image. It may be corrupt or unsupported."
        )

    return image


def enhance_contrast(image):
    """Improve local contrast using CLAHE."""

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    l_enhanced = clahe.apply(l)

    merged = cv2.merge(
        (l_enhanced, a, b)
    )

    return cv2.cvtColor(
        merged,
        cv2.COLOR_LAB2BGR
    )


def correct_brightness(image, target_mean=130.0):
    """Automatically adjust image brightness using gamma correction."""

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    current_mean = max(
        1.0,
        float(np.mean(gray))
    )

    gamma = (
        np.log(target_mean / 255.0)
        / np.log(current_mean / 255.0)
    )

    gamma = np.clip(
        gamma,
        0.3,
        3.0
    )

    table = np.array(
        [
            ((i / 255.0) ** gamma) * 255
            for i in range(256)
        ]
    ).astype("uint8")

    return cv2.LUT(
        image,
        table
    )


def denoise(image):
    """Reduce noise while preserving image details."""

    return cv2.fastNlMeansDenoisingColored(
        image,
        None,
        h=7,
        hColor=7,
        templateWindowSize=7,
        searchWindowSize=21
    )


def sharpen(image):
    """Make edges and image details clearer."""

    blurred = cv2.GaussianBlur(
        image,
        (0, 0),
        sigmaX=3
    )

    return cv2.addWeighted(
        image,
        1.5,
        blurred,
        -0.5,
        0
    )


def upscale(image, scale=2):
    """Increase image resolution using cubic interpolation."""

    height, width = image.shape[:2]

    new_width = width * scale
    new_height = height * scale

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_CUBIC
    )


def enhance_image(input_path, output_dir):

    # Check whether input file exists
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"File not found: {input_path}"
        )

    # Check file format
    extension = os.path.splitext(
        input_path
    )[1].lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported image format: {extension}"
        )

    # Load image
    image = load_image(input_path)

    # Create Output folder if it doesn't exist
    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # 1. Contrast Enhancement
    contrast_enhanced = enhance_contrast(image)

    cv2.imwrite(
        os.path.join(
            output_dir,
            "contrast_enhanced.jpg"
        ),
        contrast_enhanced
    )

    # 2. Brightness Correction
    brightness_corrected = correct_brightness(image)

    cv2.imwrite(
        os.path.join(
            output_dir,
            "brightness_corrected.jpg"
        ),
        brightness_corrected
    )

    # 3. Noise Reduction
    denoised = denoise(image)

    cv2.imwrite(
        os.path.join(
            output_dir,
            "denoised.jpg"
        ),
        denoised
    )

    # 4. Sharpening
    sharpened = sharpen(image)

    cv2.imwrite(
        os.path.join(
            output_dir,
            "sharpened.jpg"
        ),
        sharpened
    )

    # 5. Upscaling
    upscaled = upscale(
        image,
        scale=2
    )

    cv2.imwrite(
        os.path.join(
            output_dir,
            "upscaled_2x.jpg"
        ),
        upscaled
    )

    # 6. Combined Enhancement
    combined = denoise(image)
    combined = correct_brightness(combined)
    combined = enhance_contrast(combined)
    combined = sharpen(combined)

    cv2.imwrite(
        os.path.join(
            output_dir,
            "fully_enhanced.jpg"
        ),
        combined
    )

    print()
    print("Image enhancement completed successfully!")
    print()
    print("Generated files:")

    output_files = [
        "contrast_enhanced.jpg",
        "brightness_corrected.jpg",
        "denoised.jpg",
        "sharpened.jpg",
        "upscaled_2x.jpg",
        "fully_enhanced.jpg"
    ]

    for file_name in output_files:
        print(f" - {file_name}")


def main():

    if len(sys.argv) != 2:

        print()
        print("Usage:")
        print(
            "python image_enhancement.py <path-to-image>"
        )

        return

    input_path = sys.argv[1]

    # Output folder is inside the Lab04 project folder
    project_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_dir = os.path.join(
        project_dir,
        "Output"
    )

    try:

        enhance_image(
            input_path,
            output_dir
        )

    except (
        FileNotFoundError,
        ValueError
    ) as error:

        print()
        print(f"Error: {error}")

    except Exception as error:

        print()
        print(
            f"Error during image processing: {error}"
        )


if __name__ == "__main__":
    main()
