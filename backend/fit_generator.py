import pandas as pd
import os
import uuid
import zipfile
from fitparse import FitFile
from fitparse.records import FileId, Workout, WorkoutStep, Time

def generate_fit_files(filepath, output_dir):
    # Lade CSV/Excel-Datei
    df = pd.read_excel(filepath) if filepath.endswith('.xlsx') else pd.read_csv(filepath)
    
    temp_dir = os.path.join(output_dir, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    for index, row in df.iterrows():
        # Erstelle FIT-Datei
        fit_file = FitFile()

        # Erstelle FileId (Metadaten für die FIT-Datei)
        file_id = FileId(
            type=0,  # 0 = Activity (Workout)
            manufacturer=1,  # Garmin
            product=123,  # Beispielprodukt-ID
            serial=12345678  # Beispielseriennummer
        )
        fit_file.add_record(file_id)

        # Erstelle das Workout
        workout = Workout(name=row['Einheit'])
        fit_file.add_record(workout)

        # Füge Schritte zum Workout hinzu
        fit_file.add_record(WorkoutStep(name='Warm-up', duration=row['Warm-up']))
        fit_file.add_record(WorkoutStep(name='Main', duration=row['Intervalle']))
        fit_file.add_record(WorkoutStep(name='Cooldown', duration=row['Cool-down']))

        # Speichere die FIT-Datei
        filename = f"{row['Datum']}_{row['Einheit'].replace(' ', '_')}.fit"
        fit_path = os.path.join(temp_dir, filename)
        fit_file.save(fit_path)

    # ZIP die FIT-Dateien
    zip_path = os.path.join(output_dir, f"workouts_{uuid.uuid4()}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(temp_dir):
            zipf.write(os.path.join(temp_dir, file), arcname=file)

    return zip_path
