import os
from datetime import datetime
import struct

def create_fit_file(workout_data):
    output_path = "backend/output/workout.fit"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as file:
        # Schreibe einen simplen Dummy-FIT-Header (garmin-unerwartete Struktur!)
        header = bytearray()
        header.extend(b"\x0E")  # Header size
        header.extend(b".FIT")  # File type
        header.extend(struct.pack("<I", 0))  # CRC Placeholder

        file.write(header)

        # Optional: Beispielhafter Inhalt
        file.write(b"\x00" * 100)  # Dummy-Inhalt

    print(f"FIT-Datei erstellt und gespeichert unter {output_path}")
