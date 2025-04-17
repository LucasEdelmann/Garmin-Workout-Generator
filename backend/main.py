from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import BytesIO
import os

# Für die Erstellung einer .FIT-Datei benötigst du eine Bibliothek
# Hier simulieren wir das Erstellen einer Datei. Du kannst später die tatsächliche Generierung integrieren.

app = FastAPI()

# Funktion zum Erstellen einer .FIT-Datei
def create_fit_file(training_plan):
    # Dies ist ein Platzhalter für die tatsächliche Logik zur FIT-Datei-Erstellung.
    # Hier könntest du die Logik einfügen, die das FIT-Format entsprechend den Trainingsdaten generiert.
    
    fit_file_name = "training_plan.fit"
    # Zum Beispiel speichern wir einfach die Trainingsplan-Daten in eine Textdatei.
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

    # Hier drucken wir die Inhalte der Excel-Datei für Debugging-Zwecke
    print(df)

    # Erstellen des Trainingsplans (dies sollte die Logik zum Konvertieren in das FIT-Format beinhalten)
    training_plan = ""
    for index, row in df.iterrows():
        training_plan += f"Phase: {row['Phase']}, Typ: {row['Typ']}, Dauer: {row['Dauer (min)']} min, Pace: {row['Pace (min/km)']}\n"

    # Erstelle eine .FIT-Datei (dieser Schritt ist aktuell ein Platzhalter)
    fit_file_path = create_fit_file(training_plan)

    # Die Datei zurückgeben (oder eine andere Antwort je nach Implementierung)
    return {"message": "FIT-Datei erstellt", "fit_file_path": fit_file_path}

# Start der FastAPI-Anwendung
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
