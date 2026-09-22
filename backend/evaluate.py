import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from pipeline import FEATURES, TARGET, build_pipeline, categorical_features

df = pd.read_csv('../data/Expanded_Car_Dataset.csv')
x = df[FEATURES]
y = df[TARGET]


def report(name, y_true, y_pred):
    print(f'{name:<28} R2 {r2_score(y_true, y_pred):.3f}   '
          f'MAE ${mean_absolute_error(y_true, y_pred):,.0f}   '
          f'MAPE {mean_absolute_percentage_error(y_true, y_pred):.1%}')


def mileage_violations(model, rows, grid=(10_000, 30_000, 60_000, 100_000, 150_000, 200_000)):
    """Share of cars whose predicted value goes up at some point as mileage increases."""
    expanded = rows.loc[rows.index.repeat(len(grid))].copy()
    expanded['mileage'] = np.tile(grid, len(rows))
    preds = model.predict(expanded).reshape(len(rows), len(grid))
    return (np.diff(preds, axis=1) > 1e-6).any(axis=1).mean()


# Random 80/20 split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = build_pipeline(x_train).fit(x_train, y_train)
report('XGBoost (held-out 20%)', y_test, model.predict(x_test))

baseline = Pipeline([
    ('preprocessor', ColumnTransformer(
        [('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')),
    ('regressor', LinearRegression()),
]).fit(x_train, y_train)
report('Linear regression baseline', y_test, baseline.predict(x_test))
report('Predict-the-mean baseline', y_test, np.full(len(y_test), y_train.mean()))

# Hold out entire car models to test generalization to cars never seen in training
groups = df['brand'] + '_' + df['model']
train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=0).split(x, y, groups))
unseen = build_pipeline(x.iloc[train_idx]).fit(x.iloc[train_idx], y.iloc[train_idx])
report('XGBoost (unseen car models)', y.iloc[test_idx], unseen.predict(x.iloc[test_idx]))

sample = x_test.sample(1000, random_state=0)
print(f'\nCars valued higher at some higher mileage: {mileage_violations(model, sample):.1%}')
