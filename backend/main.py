from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import struct

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Route für die Startseite (liefert index.html aus)
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")

# Funktion zum Erstellen der Garmin FIT-Datei
def create_garmin_fit(training_data):
    # Erstellen eines Basis-Header für die FIT-Datei
    header = b"FIT"
    file_type = struct.pack("B", 0)  # 0 = Aktivität
    protocol_version = struct.pack("B", 2)  # Protocol Version
    
    # Einfache Header-Daten für den Anfang
    header_data = header + file_type + protocol_version
    
    # Erstellen einer List der Trainingsphasen
    activities = []
    for phase in training_data:
        phase_data = f"Phase: {phase['Phase']}, Typ: {phase['Typ']}, Dauer: {phase['Dauer']} min, Pace: {phase['Pace']}\n"
        activities.append(phase_data)
    
    # Konvertieren der Trainingsphasen in Bytes
    activity_data = b"".join([phase.encode("utf-8") for phase in activities])

    # Generieren des finalen FIT-File-Inhalts
    fit_data = header_data + activity_data

    # Speichern der FIT-Datei im aktuellen Verzeichnis
    fit_file_path = "frontend/static/training_plan.fit"
    with open(fit_file_path, "wb") as f:
        f.write(fit_data)

    return fit_file_path

# Route zum Hochladen der Excel-Datei und Erstellen der .FIT-Datei
@app.post("/create_fit/")
async def create_fit(file: UploadFile = File(...)):
    # Die Excel-Datei aus dem Upload lesen
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Verarbeite die Excel-Daten (hier als Textzusammenfassung, kann weiter angepasst werden)
    training_data = []
    for index, row in df.iterrows():
        phase = {
            "Phase": row['Phase'],
            "Typ": row['Typ'],
            "Dauer": row['Dauer (min)'],
            "Pace": f"{row['Pace (min/km)'].split('-')[0]} - {row['Pace (min/km)'].split('-')[1]}"
        }
        training_data.append(phase)

    # Erstelle die .FIT-Datei
    fit_file_path = create_garmin_fit(training_data)

    return {"message": "FIT-Datei erstellt", "fit_file_path": fit_file_path}
