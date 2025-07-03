import pandas as pd 
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv('../data/cars.csv')

x = df[['year', 'mileage', 'purchsase_price']]
y = df[['current_value']]

model = LinearRegression()
model.fit(x, y)

joblib.dump(model, 'model.pkl')
print('Model trained and saved as model.pkl')