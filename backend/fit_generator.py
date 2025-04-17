import os
from garminfit import FitFile

def create_fit_file():
    # Erstelle eine neue FIT-Datei
    fit_file = FitFile()

    # Beispiel: Workout-Details (passen Sie diese an Ihre Datenstruktur an)
    fit_file.add_record('FileId', {'type': 1, 'manufacturer': 1, 'product': 123})
    fit_file.add_record('Workout', {'name': 'Test Workout'})
    fit_file.add_record('WorkoutStep', {'name': 'Warm-up', 'duration': 5})
    fit_file.add_record('WorkoutStep', {'name': 'Main', 'duration': 20})
    fit_file.add_record('WorkoutStep', {'name': 'Cooldown', 'duration': 5})

    # Speichern der FIT-Datei
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    fit_path = os.path.join(output_dir, 'test_workout.fit')
    fit_file.save(fit_path)

    print(f"FIT-Datei gespeichert unter: {fit_path}")
