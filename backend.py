# backend.py

import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from paper_processing import extract_text_from_pdf, summarize_and_generate_script
from podcast_generation import generate_podcast_audio
from utils import save_uploaded_file, get_temporary_file_path

# Initialize FastAPI app
app = FastAPI()

# Configuration
API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("Google Gemini API key is not set")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define API models
class UploadResponse(BaseModel):
    file_id: str
    status: str

class ProcessingStatus(BaseModel):
    file_id: str
    status: str

# Workflow function
def process_paper(file_path):
    try:
        # Step 1: Extract text from PDF
        text = extract_text_from_pdf(file_path)

        # Step 2: Summarize and generate script
        script = summarize_and_generate_script(text, API_KEY)

        # Step 3: Generate podcast audio
        audio_path = generate_podcast_audio(script)

        return audio_path
    except Exception as e:
        logger.error(f"Error processing paper: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# API endpoints
@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_uploaded_file(file)
        file_id = os.path.basename(file_path)
        return UploadResponse(file_id=file_id, status="Uploaded")
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/status/{file_id}", response_model=ProcessingStatus)
async def get_status(file_id: str):
    try:
        # Check processing status (simplified example)
        status = "Processing"  # In a real implementation, check the actual status
        return ProcessingStatus(file_id=file_id, status=status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/play/{file_id}")
async def play_podcast(file_id: str):
    try:
        # Retrieve and return the podcast audio (simplified example)
        audio_path = get_temporary_file_path(file_id)
        return FileResponse(audio_path, media_type="audio/mpeg")
    except Exception as e:
        logger.error(f"Error playing podcast: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)