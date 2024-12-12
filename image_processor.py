import cv2
import numpy as np
from PIL import Image
from rembg import remove
import requests
from io import BytesIO
from utils import upload_to_drive  # Import the upload function from utils.py

def process_image(image_url, bounding_box):
    """
    Processes the given image URL and removes the background of the specified bounding box.
    """
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except RequestException as e:
        raise Exception(f"Failed to fetch the image: {e}")
    # Step 1: Download the image
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch the image from the provided URL.")
    image = Image.open(BytesIO(response.content))
    
    # Step 2: Crop the bounding box
    x_min, y_min, x_max, y_max = bounding_box.values()
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    
    # Step 3: Apply background removal
    cropped_image_bytes = BytesIO()
    cropped_image.save(cropped_image_bytes, format="PNG")
    cropped_image_bytes = cropped_image_bytes.getvalue()
    output = remove(cropped_image_bytes)

    # Step 4: Save processed image
    processed_image_path = "processed_image.png"
    with open(processed_image_path, "wb") as f:
        f.write(output)

    # Step 5: Upload to Google Drive and return the public URL
    public_url = upload_to_drive(processed_image_path, "processed_image.png")
    
    return public_url  # Return the public URL from Google Drive
