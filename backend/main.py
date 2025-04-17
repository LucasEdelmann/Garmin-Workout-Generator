from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from backend.fit_generator import generate_fit_files


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile):
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    zip_path = generate_fit_files(filepath, OUTPUT_DIR)
    return {"download_url": f"/download/{os.path.basename(zip_path)}"}

@app.get("/download/{zip_filename}")
async def download_zip(zip_filename: str):
    return FileResponse(os.path.join(OUTPUT_DIR, zip_filename), media_type="application/zip", filename=zip_filename)
