import pandas as pd 
from xgboost import XGBRegressor
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv('../data/Expanded_Car_Dataset.csv')

y = df['current_value']

x = df[['brand', 'model', 'year', 'mileage', 'drivetrain', 'msrp',]]

categorical_features = ['brand', 'model', 'drivetrain']
numeric_features = ['year', 'mileage', 'msrp',]

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators=100, random_state=42, verbosity=0))
])

pipeline.fit(x, y)

joblib.dump(pipeline, 'model.pkl')
print('Model trained and saved as model.pkl')