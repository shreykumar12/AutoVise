from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

FEATURES = ['brand', 'model', 'year', 'mileage', 'drivetrain', 'msrp']
TARGET = 'current_value'

categorical_features = ['brand', 'model', 'drivetrain']
numeric_features = ['year', 'mileage', 'msrp']

# -1 forces predictions to never increase as the feature increases
MONOTONE = {'mileage': -1}


def build_pipeline(x):
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numeric_features),
        ]
    )
    # XGBoost takes one constraint per encoded column, so fit the encoder first to know the width
    n_encoded = preprocessor.fit(x).transform(x[:1]).shape[1]
    n_categorical = n_encoded - len(numeric_features)
    constraints = [0] * n_categorical + [MONOTONE.get(f, 0) for f in numeric_features]

    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(
            n_estimators=100,
            random_state=42,
            verbosity=0,
            monotone_constraints=tuple(constraints),
        ))
    ])
