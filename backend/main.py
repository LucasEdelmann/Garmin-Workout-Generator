from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import os
import xml.etree.ElementTree as ET

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Route für die Startseite (liefert index.html aus)
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")


# Funktion zum Erstellen einer TCX-Datei
def create_tcx_file(training_plan):
    # Erstelle den Ordner, falls er nicht existiert
    output_dir = "frontend/static"
    os.makedirs(output_dir, exist_ok=True)  # Dieser Schritt stellt sicher, dass der Ordner existiert
    
    # Erstelle die XML-Struktur
    tcx = ET.Element("TrainingCenterDatabase", xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")

    # Workout-Tag erstellen
    workouts = ET.SubElement(tcx, "Workouts")
    
    for phase in training_plan:
        workout = ET.SubElement(workouts, "Workout", Sport="Running")
        
        # Informationen zur Phase hinzufügen
        activity = ET.SubElement(workout, "Step", Type="Time")
        duration = ET.SubElement(activity, "Duration")
        duration.text = str(phase['Dauer'])
        
        pace = ET.SubElement(activity, "Pace")
        pace.text = str(phase['Pace'])
        
    # Dateipfad für TCX-Datei
    tcx_file_name = os.path.join(output_dir, "training_plan.tcx")
    
    # Speichern der XML-Datei
    tree = ET.ElementTree(tcx)
    tree.write(tcx_file_name)
    
    return tcx_file_name


# Route zum Hochladen der Excel-Datei und Erstellen der TCX-Datei
@app.post("/create_tcx/")
async def create_tcx(file: UploadFile = File(...)):
    # Die Excel-Datei aus dem Upload lesen
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Trainingsplan verarbeiten
    training_plan = []
    for index, row in df.iterrows():
        phase_info = {
            "Phase": row['Phase'],
            "Typ": row['Typ'],
            "Dauer": row['Dauer (min)'],
            "Pace": row['Pace (min/km)'],
        }
        training_plan.append(phase_info)

    # Erstelle die TCX-Datei
    tcx_file_path = create_tcx_file(training_plan)

    return {"message": "TCX-Datei erstellt", "tcx_file_path": tcx_file_path}
