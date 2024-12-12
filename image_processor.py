import cv2
import numpy as np
from PIL import Image
from rembg import remove
import requests
from io import BytesIO
from utils import upload_to_drive  # Import the upload function from utils.py
import os
def process_image(image_url, bounding_box):
    """
    Processes the given image URL, crops the image based on the bounding box,
    removes the background from the cropped area, saves it, and uploads it to Google Drive.

    Args:
        image_url (str): URL of the image to be processed.
        bounding_box (dict): Dictionary with bounding box coordinates in the format:
                             {"x_min": 0, "y_min": 0, "x_max": 100, "y_max": 100}
                             These coordinates specify the region to crop.

    Returns:
        str: Public URL of the uploaded file on Google Drive.
    """
    try:
        # Step 1: Download the image from the URL
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        image = Image.open(BytesIO(response.content))
        print(f"Image successfully fetched from {image_url}")

        # Step 2: Crop the image based on the bounding box
        x_min, y_min, x_max, y_max = bounding_box["x_min"], bounding_box["y_min"], bounding_box["x_max"], bounding_box["y_max"]
        cropped_image = image.crop((x_min, y_min, x_max, y_max))
        print(f"Image successfully cropped using bounding box: {bounding_box}")

        # Step 3: Apply background removal using rembg
        cropped_image_bytes = BytesIO()
        cropped_image.save(cropped_image_bytes, format="PNG")
        cropped_image_bytes = cropped_image_bytes.getvalue()
        output = remove(cropped_image_bytes)  # Remove the background
        
        # Step 4: Save the processed image to disk
        processed_image_path = "processed_image.png"
        with open(processed_image_path, "wb") as f:
            f.write(output)
        print(f"Processed image saved to {processed_image_path}")

        # Step 5: Check if the file exists before uploading
        if not os.path.exists(processed_image_path):
            print(f"Error: The file {processed_image_path} was not created or saved properly.")
            return None
        
        # Step 6: Upload the processed image to Google Drive and get the public URL
        public_url = upload_to_drive(processed_image_path, "processed_image.png")
        
        if public_url:
            print(f"Image uploaded successfully! Public URL: {public_url}")
        else:
            print(f"Failed to upload image or get public URL.")
        
        return public_url
    
    except requests.RequestException as e:
        print(f"Error downloading the image: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        return None
