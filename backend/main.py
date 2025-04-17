from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import os

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Route für die Startseite (liefert index.html aus)
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")

# Funktion zum Erstellen einer .tcx-Datei
def create_tcx_file(training_plan):
    # Hier erstellen wir eine einfache TCX-Datei (kann weiter verfeinert werden)
    tcx_file_name = "frontend/static/training_plan.tcx"  # Richtige Endung verwenden
    with open(tcx_file_name, 'w') as file:
        file.write(f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        file.write("<TrainingCenterDatabase xmlns=\"http://www.garmin.com/xmlschemas/trainingcenter/v2\">\n")
        file.write("<Activities>\n")
        file.write(f"<Activity Sport=\"Running\">\n")
        file.write(f"<Id>{training_plan}</Id>\n")
        file.write(f"</Activity>\n")
        file.write("</Activities>\n")
        file.write("</TrainingCenterDatabase>\n")
    
    return tcx_file_name

# Route zum Hochladen der Excel-Datei und Erstellen der .tcx-Datei
@app.post("/create_tcx/")
async def create_tcx(file: UploadFile = File(...)):
    # Die Excel-Datei aus dem Upload lesen
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Verarbeite die Excel-Daten (hier als Textzusammenfassung, kann weiter angepasst werden)
    training_plan = ""
    for index, row in df.iterrows():
        training_plan += f"Phase: {row['Phase']}, Typ: {row['Typ']}, Dauer: {row['Dauer (min)']} min, Pace: {row['Pace (min/km)']}\n"

    # Erstelle die .tcx-Datei
    tcx_file_path = create_tcx_file(training_plan)

    return {"message": "TCX-Datei erstellt", "tcx_file_path": f"/static/training_plan.tcx"}
