from fastapi import FastAPI
from .fit_generator import create_fit_file

app = FastAPI()

@app.get("/create_fit")
def create_fit():
    # Dummy Workout-Daten
    workout_data = {
        "name": "Intervalltraining",
        "steps": [
            {"duration": 60, "name": "Warmup"},
            {"duration": 120, "name": "Sprint"},
        ]
    }
    create_fit_file(workout_data)
    return {"message": "FIT-Datei wurde erfolgreich erstellt."}
