from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import os

from .fit_generator import create_fit_file

app = FastAPI()

# Statische Dateien mounten (z. B. script.js, style.css)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Route für die Startseite (liefert index.html aus)
@app.get("/")
async def get_home():
    return FileResponse("frontend/index.html")


# Funktion zum Erstellen einer .FIT-Datei
def create_fit_file(training_plan):
    # Hier wird eine einfache FIT-Datei erstellt (als Textdatei).
    fit_file_name = "training_plan.fit"
    with open(fit_file_name, 'w') as file:
        file.write(f"Training Plan - {training_plan}\n")
        file.write("Weitere FIT-Daten würden hier folgen.\n")
    
    return fit_file_name

# Route zum Hochladen der Excel-Datei und Erstellen der .FIT-Datei
@app.post("/create_fit/")
async def create_fit(file: UploadFile = File(...)):
    # Die Excel-Datei aus dem Upload lesen
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Verarbeite die Excel-Daten (hier als Textzusammenfassung, kann weiter angepasst werden)
    training_plan = ""
    for index, row in df.iterrows():
        training_plan += f"Phase: {row['Phase']}, Typ: {row['Typ']}, Dauer: {row['Dauer (min)']} min, Pace: {row['Pace (min/km)']}\n"

    # Erstelle die .FIT-Datei
    fit_file_path = create_fit_file(training_plan)

    return {"message": "FIT-Datei erstellt", "fit_file_path": fit_file_path}
