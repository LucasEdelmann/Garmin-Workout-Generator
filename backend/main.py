import os
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Route für die Startseite (liefert index.html aus)
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")

# Funktion zum Erstellen einer .tcx-Datei
def create_tcx_file(training_plan):
    # Verzeichnis für die statischen Dateien, in dem die Datei gespeichert wird
    static_dir = "frontend/static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Die TCX-Datei erstellen und sicherstellen, dass sie die richtige Endung hat
    tcx_file_name = os.path.join(static_dir, "training_plan.tcx")
    with open(tcx_file_name, 'w') as file:
        file.write(f"<?xml version='1.0' encoding='UTF-8'?>\n")
        file.write(f"<TrainingPlan>\n")
        file.write(f"    <Details>{training_plan}</Details>\n")
        file.write(f"</TrainingPlan>\n")

    return tcx_file_name

# Route zum Hochladen der Excel-Datei und Erstellen der .TCX-Datei
@app.post("/create_tcx/")
async def create_tcx(file: UploadFile = File(...)):
    # Die Excel-Datei aus dem Upload lesen
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Verarbeite die Excel-Daten (hier als Textzusammenfassung, kann weiter angepasst werden)
    training_plan = ""
    for index, row in df.iterrows():
        training_plan += f"Phase: {row['Phase']}, Typ: {row['Typ']}, Dauer: {row['Dauer (min)']} min, Pace: {row['Pace (min/km)']}\n"

    # Erstelle die TCX-Datei
    tcx_file_path = create_tcx_file(training_plan)

    # Gebe den Pfad der Datei zurück, sodass der Client den Link nutzen kann
    return {"message": "TCX-Datei erstellt", "tcx_file_path": "training_plan.tcx"}
