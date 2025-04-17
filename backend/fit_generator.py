# backend/fit_generator.py
import struct
import os

# Schritt 1: Header einer FIT-Datei erstellen
def write_header(file):
    header = b"FIT"  # Dateiflags
    header_version = struct.pack('B', 1)  # Versionsnummer (1 Byte)
    header_type = struct.pack('B', 0)  # Dateityp: 0 für Standard
    file.write(header)
    file.write(header_version)
    file.write(header_type)

# Schritt 2: Fitness-Daten (wie Trainingsschritte) hinzufügen
def write_workout(file, workout_name, steps):
    for step in steps:
        step_name = step['name'].encode('utf-8')
        step_duration = struct.pack('I', step['duration'])  # Dauer als Integer (4 Bytes)
        step_type = struct.pack('B', step['type'])  # Typ als Byte (1 Byte)
        file.write(step_name)
        file.write(step_duration)
        file.write(step_type)

# Schritt 3: Footer einer FIT-Datei erstellen
def write_footer(file):
    footer = b"END"  # Einfacher Footer
    file.write(footer)

# Hauptfunktion zum Erstellen der FIT-Datei
def create_fit_file(workout_data, output_path="backend/output/workout.fit"):
  

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "wb") as file:

    write_header(file)
    write_workout(file, workout_data['name'], workout_data['steps'])
    write_footer(file)
    print(f"FIT-Datei erstellt und gespeichert unter {output_path}")
