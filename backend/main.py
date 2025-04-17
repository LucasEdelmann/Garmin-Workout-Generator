from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Statische Dateien (Frontend) laden
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Route zum Hochladen der Datei
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Definiere den Speicherort für die hochgeladene Datei
    file_location = f"uploaded_files/{file.filename}"

    # Speichern der hochgeladenen Datei
    Path("uploaded_files").mkdir(parents=True, exist_ok=True)  # Stelle sicher, dass der Ordner existiert
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Hier kannst du die Datei dann weiter verarbeiten
    # Zum Beispiel in eine FIT-Datei umwandeln

    return {"message": f"Die Datei {file.filename} wurde erfolgreich hochgeladen."}

# Route zum Herunterladen der generierten FIT-Datei
@app.get("/download")
def download_fit():
    # Gib hier den richtigen Pfad zur erzeugten FIT-Datei an
    file_path = "uploaded_files/workout.fit"  # Beispielhafte Pfadangabe
    return FileResponse(file_path, media_type='application/octet-stream', filename="workout.fit")
