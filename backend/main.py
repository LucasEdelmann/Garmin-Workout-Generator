# backend/main.py
from fastapi import FastAPI
from .fit_generator import create_fit_file


app = FastAPI()

# Beispiel-Workout-Daten
workout_data = {
    'name': 'Morning Run',
    'steps': [
        {'name': 'Warm-up', 'duration': 5, 'type': 1},  # Warm-up, 5 Minuten, Typ 1
        {'name': 'Main Run', 'duration': 20, 'type': 2},  # Hauptlauf, 20 Minuten, Typ 2
        {'name': 'Cooldown', 'duration': 5, 'type': 3}  # Cooldown, 5 Minuten, Typ 3
    ]
}

import logging
logging.basicConfig(level=logging.INFO)
...

@app.get("/create_fit")
def create_fit():
    logging.info("FIT-Erstellung gestartet")
    create_fit_file(workout_data)
    logging.info("FIT-Erstellung abgeschlossen")
    return {"message": "FIT-Datei wurde erfolgreich erstellt."}
