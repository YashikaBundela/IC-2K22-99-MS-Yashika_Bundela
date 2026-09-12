import cv2
import os
import sys
SUPPORTED_FORMATS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"
}
def process_image(input_path, output_dir):
    """Apply basic image processing operations."""
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Unable to load image.")
        return
    os.makedirs(output_dir, exist_ok=True)
    # 1. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(output_dir, "grayscale.jpg"), gray)
    # 2. Resize to 50% of original dimensions
    height, width = image.shape[:2]
    resized = cv2.resize(image, (width // 2, height // 2))
    cv2.imwrite(os.path.join(output_dir, "resized.jpg"), resized)
    # 3. Binary Thresholding
    _, threshold = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY
    )
    cv2.imwrite(
        os.path.join(output_dir, "threshold.jpg"),
        threshold
    )
    # 4. Gaussian Blur
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    cv2.imwrite(
        os.path.join(output_dir, "blurred.jpg"),
        blurred
    )
    # 5. Edge Detection
    edges = cv2.Canny(gray, 100, 200)
    cv2.imwrite(
        os.path.join(output_dir, "edges.jpg"),
        edges
    )
    # 6. Rotate 90 degrees clockwise
    rotated = cv2.rotate(
        image,
        cv2.ROTATE_90_CLOCKWISE
    )
    cv2.imwrite(
        os.path.join(output_dir, "rotated.jpg"),
        rotated
    )
    print("\nImage processing completed successfully.")
    print("\nGenerated outputs:")
    outputs = [
        "grayscale.jpg",
        "resized.jpg",
        "threshold.jpg",
        "blurred.jpg",
        "edges.jpg",
        "rotated.jpg"
    ]
    for filename in outputs:
        print(f" - {filename}")
def main():
    if len(sys.argv) != 2:
        print("\nUsage:")
        print("python image_processing.py <image_path>")
        return
    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print("\nError: Input image does not exist.")
        return
    extension = os.path.splitext(input_path)[1].lower()
    if extension not in SUPPORTED_FORMATS:
        print("\nError: Unsupported image format.")
        print(
            "Supported formats: "
            "JPG, JPEG, PNG, BMP, WEBP, TIF, TIFF"
        )
        return
    # Cluster02-Image-Processing/output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(input_path)),
        "output"
    )
    process_image(input_path, output_dir)
if __name__ == "__main__":
    main()
