from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from image_processor import process_image
from utils import upload_to_drive

app = FastAPI(title="Background Removal API", version="1.0")

class ImageRequest(BaseModel):
    image_url: str
    bounding_box: dict

@app.post("/remove-background")
async def remove_background(request: ImageRequest, background_tasks: BackgroundTasks):
    try:
        # Validate bounding box
        if not all(key in request.bounding_box for key in ("x_min", "y_min", "x_max", "y_max")):
            raise ValueError("Invalid bounding box coordinates.")

        # Process the image
        processed_path = process_image(request.image_url, request.bounding_box)

        # Schedule upload as a background task
        background_tasks.add_task(upload_to_drive, processed_path, "processed_image.png")

        # Generate public URL immediately after upload
        processed_url = upload_to_drive(processed_path, "processed_image.png")

        return {
            "original_image_url": request.image_url,
            "processed_image_url": processed_url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
if __name__ == "__main__":
    # Get the port from the environment variable or use a default port (e.g., 8000)
    port = int(os.getenv("PORT", 8000))  # Render automatically sets the PORT variable
    uvicorn.run(app, host="0.0.0.0", port=port)
