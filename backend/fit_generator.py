```python
import pandas as pd
import os, uuid, zipfile
from fitencode import FitEncoder_Workout, FitEncoder_WorkoutStep

def generate_fit_files(filepath, output_dir):
    df = pd.read_excel(filepath) if filepath.endswith('.xlsx') else pd.read_csv(filepath)

    temp_dir = os.path.join(output_dir, str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    for index, row in df.iterrows():
        filename = f"{row['Datum']}_{row['Einheit'].replace(' ', '_')}.fit"
        path = os.path.join(temp_dir, filename)

        enc = FitEncoder_Workout(workout_name=row['Einheit'])
        enc.add_step(FitEncoder_WorkoutStep('Warmup', row['Warm-up']))
        enc.add_step(FitEncoder_WorkoutStep('Main', row['Intervalle']))
        enc.add_step(FitEncoder_WorkoutStep('Cooldown', row['Cool-down']))

        with open(path, 'wb') as f:
            f.write(enc.build_file())

    zip_path = os.path.join(output_dir, f"workouts_{uuid.uuid4()}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(temp_dir):
            zipf.write(os.path.join(temp_dir, file), arcname=file)

    return zip_path
```
