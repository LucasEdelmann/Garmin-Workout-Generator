import os
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Route für die Startseite
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")


# Funktion zum Erstellen der TCX-Datei
def create_tcx_file(training_plan):
    # Hier wird das statische Verzeichnis überprüft und sichergestellt, dass es existiert
    output_dir = 'frontend/static'
    os.makedirs(output_dir, exist_ok=True)

    # Der Name der TCX-Datei
    tcx_file_name = os.path.join(output_dir, "training_plan.tcx")

    # Erstelle die TCX-Datei
    with open(tcx_file_name, 'w') as file:
        file.write(f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        file.write("<TrainingCenterDatabase xmlns=\"http://www.garmin.com/xmlschemas/trainingcenter/v2\">\n")
        file.write("<Activities>\n")
        file.write(f"<Activity Sport=\"Running\">\n")
        file.write(f"<Id>{training_plan}</Id>\n")
        file.write(f"</Activity>\n")
        file.write("</Activities>\n")
        file.write("</TrainingCenterDatabase>\n")
    
    # Rückgabe des relativen Pfads zur erstellten Datei
    return os.path.relpath(tcx_file_name, 'frontend/static')


# Route zum Hochladen der Excel-Datei und Erstellen der TCX-Datei
@app.post("/create_tcx/")
async def create_tcx(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Hier wird die Excel-Datei verarbeitet
    training_plan = ""
    for index, row in df.iterrows():
        training_plan += f"Phase: {row['Phase']}, Typ: {row['Typ']}, Dauer: {row['Dauer (min)']} min, Pace: {row['Pace (min/km)']}\n"

    # Erstelle die TCX-Datei und gib den Pfad zurück
    tcx_file_path = create_tcx_file(training_plan)

    return {"message": "TCX-Datei erstellt", "tcx_file_path": tcx_file_path}
