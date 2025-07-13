from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
import pandas as pd

model = joblib.load('model.pkl')

app = Flask(__name__)
CORS(app)  
@app.route('/')
def home():
    return "AutoROI is live!!"
    
@app.route('/predict', methods=["POST"])
def predict():
    data = request.get_json()
    required_fields = ['year', 'mileage', 'brand', 'model', 'drivetrain', 'msrp']
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            return jsonify({'error': f'Missing or empty input: {field}'}), 400
    print('REQUEST DATA:', data)
    
    try:
        year = float(data['year'])
        mileage = float(data['mileage'])
        brand = str(data['brand'])
        model_name = str(data['model'])
        drivetrain = str(data['drivetrain'])
        msrp = float(data['msrp'])
        
        if year < 0 or mileage < 0 or msrp < 0:
            return jsonify({'error': 'Inputs must be non-negative numerical values.'}), 400
        
        features = pd.DataFrame([{
            "brand": brand,
            "model": model_name,
            "year": year,
            "mileage": mileage,
            "drivetrain": drivetrain,
            "msrp": msrp
        }])
        raw_prediction = model.predict(features)[0]
        predicted_value = float(max(0.0, raw_prediction))  
        
        return jsonify({
            'predicted_value': round(predicted_value, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)