import pandas as pd
import joblib
from pipeline import FEATURES, TARGET, build_pipeline

df = pd.read_csv('../data/Expanded_Car_Dataset.csv')

x = df[FEATURES]
y = df[TARGET]

pipeline = build_pipeline(x)
pipeline.fit(x, y)

joblib.dump(pipeline, 'model.pkl')
print('Model trained and saved as model.pkl')
