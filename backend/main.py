from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .fit_generator import create_fit_file

app = FastAPI()

# Statische Dateien (Frontend) laden
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.get("/create_fit")
def create_fit():
    workout_data = {
        "name": "Intervalltraining",
        "steps": [
            {"duration": 60, "name": "Warmup"},
            {"duration": 120, "name": "Sprint"},
        ]
    }
    create_fit_file(workout_data)
    return {"message": "FIT-Datei wurde erfolgreich erstellt."}
