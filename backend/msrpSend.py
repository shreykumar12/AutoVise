import os
import pandas as pd
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend folder
CSV_PATH = os.path.join(BASE_DIR, 'data', 'Expanded_Car_Dataset.csv')
DEST_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'src')
OUT_PATH = os.path.join(DEST_DIR, 'msrp_data.json')


if not os.path.isfile(CSV_PATH):
    raise FileNotFoundError(f"CSV not found at {CSV_PATH}")
df = pd.read_csv(CSV_PATH)


df['key'] = df['brand'] + '_' + df['model'] + '_' + df['year'].astype(str)
msrp_map = df.groupby('key')['msrp'].mean().round().astype(int).to_dict()


os.makedirs(DEST_DIR, exist_ok=True)


with open(OUT_PATH, 'w') as f:
    json.dump(msrp_map, f, indent=2)

print(f"✅ msrp_data.json created successfully at {OUT_PATH} with {len(msrp_map)} entries")