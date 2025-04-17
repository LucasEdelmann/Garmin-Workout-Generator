import pandas as pd
import os
import uuid
import zipfile
from fit_sdk import FitFile, FitRecord, FitMessage, FitField

def generate_fit_files(filepath, output_dir):
    # Lade CSV/Excel-Datei
    df = pd.read_excel(filepath) if filepath.endswith('.xlsx') else pd.read_csv(filepath)
    
    temp_dir = os.path.join(output_dir, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    for index, row in df.iterrows():
        # Erstelle FIT-Datei
        fit_file = FitFile()

        # Erstelle eine Datei und eine Aktivität
        file_record = FitRecord(message_type="file_id")
        file_record.add_field(FitField(name="type", value=0))  # 0 = Activity
        file_record.add_field(FitField(name="manufacturer", value=1))  # Garmin
        file_record.add_field(FitField(name="product", value=123))  # Produkt-ID
        file_record.add_field(FitField(name="serial", value=12345678))  # Seriennummer
        fit_file.add_record(file_record)

        # Erstelle das Workout
        workout_record = FitRecord(message_type="workout")
        workout_record.add_field(FitField(name="name", value=row['Einheit']))
        fit_file.add_record(workout_record)

        # Füge Schritte zum Workout hinzu
        fit_file.add_record(FitRecord(message_type="workout_step", fields=[
            FitField(name="name", value="Warm-up"),
            FitField(name="duration", value=row['Warm-up'])
        ]))
        fit_file.add_record(FitRecord(message_type="workout_step", fields=[
            FitField(name="name", value="Main"),
            FitField(name="duration", value=row['Intervalle'])
        ]))
        fit_file.add_record(FitRecord(message_type="workout_step", fields=[
            FitField(name="name", value="Cooldown"),
            FitField(name="duration", value=row['Cool-down'])
        ]))

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
