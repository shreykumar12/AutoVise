from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

model = joblib.load('model.pkl')

app = Flask(__name__)
CORS(app)  
@app.route('/')
def home():
    return "AutoROI is live!!"
    
@app.route('/predict', methods=["POST"])
def predict():
    data = request.get_json()
    required_fields = ['year', 'mileage', 'purchase_price']
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            return jsonify({'error': f'Missing or empty input: {field}'}), 400
    print('REQUEST DATA:', data)
    
    try:
        year = float(data['year'])
        mileage = float(data['mileage'])
        purchase_price = float(data['purchase_price'])
        
        if year < 0 or mileage < 0 or purchase_price < 0:
            return jsonify({'error': 'Inputs must be non-negative numerical values.'}), 400
        
        features = np.array([[year, mileage, purchase_price]])
        predicted_value = float(model.predict(features)[0])
        
        roi = ((predicted_value - purchase_price) / purchase_price) *100
        
        return jsonify({
            'predicted_value': round(predicted_value,2),
            'roi': round(roi, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)