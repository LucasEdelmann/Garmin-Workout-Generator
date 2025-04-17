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


# Funktion zum Erstellen einer .FIT-Datei
def create_fit_file(training_plan):
    # Sicherstellen, dass der 'static' Ordner existiert
    static_dir = "frontend/static"
    os.makedirs(static_dir, exist_ok=True)

    # Den Dateinamen dynamisch erstellen
    fit_file_name = "training_plan.fit"
    fit_file_path = os.path.join(static_dir, fit_file_name)

    # Erstelle die FIT-Datei im richtigen Ordner
    with open(fit_file_path, 'w') as file:
        file.write(f"Training Plan - {training_plan}\n")
        file.write("Weitere FIT-Daten würden hier folgen.\n")
    
    return fit_file_path

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

    # Gebe den relativen Pfad der Datei zurück, um sie im Frontend zum Download anzubieten
    return {"message": "FIT-Datei erstellt", "fit_file_path": f"/static/{os.path.basename(fit_file_path)}"}
